# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
from entrodec.component.yaml.parser import YamlParser
from entrodec.component.di.compiler import Compiler, Importer
from entrodec.component.di.dispatcher import ServiceManagement
import os
import sys

__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'

os.environ.setdefault('APPLICATION_NAME', 'app')
#os.environ.setdefault('APPLICATION_MODE', 'production')
os.environ.setdefault('APPLICATION_MODE', 'development')

if os.environ.get('APPLICATION_MODE') == 'development':
    # TODO: add watch task for changes
    # 1) if configs was changed - then recompile bootstrap and restart server
    # 2) if any other source was changed - then just restart server
    application = Importer.import_module(os.environ.get('APPLICATION_NAME'))
    application_folder = os.path.dirname(application.__file__)
    config = YamlParser.parse_file_by_path(file_path=application_folder + '/config/config.yml')
    YamlParser.save(data=config, file_path=application_folder + '/cache/config.py')
    Compiler.compile(config=config, output_file_path=application_folder + '/cache/bootstrap.py')


class Request:
    path_info = '/'
    query_string = ''
    full_path = ''

    def __init__(self, environ):
        self.path_info = environ.get('PATH_INFO')
        self.query_string = environ.get('QUERY_STRING')
        self.full_path = self.path_info + ('?' + self.query_string if self.query_string else '')




from wsgiref.util import setup_testing_defaults, request_uri
from wsgiref.simple_server import make_server

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = str('200 OK')
    headers = [(str('Content-type'), str('text/html'))]

    start_response(status, headers)
    return [str(ServiceManagement.dispatch(Request(environ)))]

httpd = make_server('', 8001, simple_app)
print "Serving on port 8001..."
httpd.serve_forever()