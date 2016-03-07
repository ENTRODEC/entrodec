# _*_ coding: utf-8 _*_
# DDN'T CHANGE THIS FILE!
from __future__ import unicode_literals
from entrodec.component.di.importer import Importer
from entrodec.component.config import get_config


def get_service_cool_service_app_modules_shop_services_test():
    module_instance = Importer.import_module("app.modules.shop.services.test")
    instance = getattr(module_instance, "test")

    return instance(**{'name': "Dmitri Mes'hin", 'value': get_service_another_service_app_modules_shop_services_test2()})


def get_service_another_service_app_modules_shop_services_test2():
    module_instance = Importer.import_module("app.modules.shop.services.test2")
    instance = getattr(module_instance, "test2")

    return instance(get_config("locale"), get_service_service3_app_modules_shop_services_test3())


def get_service_service3_app_modules_shop_services_test3():
    module_instance = Importer.import_module("app.modules.shop.services.test3")
    instance = getattr(module_instance, "test3class")
    instance = instance(**{'some': 'object'})
    instance.testmethod('test param', 'test param2')
    instance.testmethod('test param3', 'test param4')
    instance.set_alchemy(get_service_sqlalchemy_sqlalchemy())
    return instance


def get_service_sqlalchemy_sqlalchemy():
    module_instance = Importer.import_module("sqlalchemy")
    instance = getattr(module_instance, "create_engine")

    return instance

