# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import importlib

__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'


class Importer:
    imported_modules = dict()

    def __init__(self):
        pass

    @classmethod
    def import_module(cls, source, parent=None):
        if not cls.imported_modules.get(source):
            imported_module = importlib.import_module(source, package=parent)
            cls.imported_modules[source] = imported_module
        return cls.imported_modules[source]