# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import os
import re
from entrodec.component.config import get_config
from entrodec.component.di.importer import Importer
from entrodec.component.response.exceptions import NotFoundException

__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'


class ServiceManagement:

    routes = None
    routes_compiled = dict()

    @classmethod
    def get_service_instance(cls, name):
        service_info = get_config('services', dict()).get(name)
        service_getter = 'get_service_' + name.replace('.', '_') + '_' + service_info.get('module').replace('.', '_')
        service_module = Importer.import_module(os.environ.get('APPLICATION_NAME') + '.cache.bootstrap')
        service = getattr(service_module, service_getter)
        return service


    @classmethod
    def dispatch(cls, request):

        if cls.routes is None:
            cls.routes = get_config('routes', dict())

        for route_name, route_config in cls.routes.items():
            namespace = route_config.get('namespace')

            for route_info in route_config.get('endpoints'):
                if namespace == '/' or not namespace:
                    path = '^/' + route_info.get('path').lstrip('/')
                else:
                    path = '^/' + namespace.strip('/') + '/' + route_info.get('path').lstrip('/')
                parameters = route_info.get('parameters', dict())

                for param_name, param_condition in parameters.items():
                    path = path.replace('{{%s}}' % param_name, param_condition)

                if not cls.routes_compiled.get(path):
                    cls.routes_compiled[path] = re.compile(path)

                if cls.routes_compiled[path].match(request.full_path):
                    service = cls.get_service_instance(route_info.get('service'))
                    # TODO: if there was url params then provide it's values to service
                    response = service()
                    return response

        raise NotFoundException(message='Can not find matched route for this url', args=[request.full_path])
