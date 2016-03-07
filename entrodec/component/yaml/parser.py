# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'

import re
import os
import pprint
from copy import deepcopy
from yaml import load, dump
from entrodec.component.di.importer import Importer
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class BaseParser:
    """
    Base configuration parser with common functions
    """

    @classmethod
    def get_file_contents_as_dict(cls, file_path):
        return dict()

    @classmethod
    def parse_file_by_path(cls, file_path):
        """
        Parsing and processing all the configuration based on root config file path
        """
        data = cls.get_file_contents_as_dict(file_path)
        data = cls.process_imports(data, file_path)
        data = cls.inject_parameters(data)
        return data

    @classmethod
    def process_imports(cls, yaml_data, file_path):
        yaml_imports = yaml_data.get('imports', list())

        if yaml_imports and type(yaml_imports) is list:

            for import_file in yaml_imports:
                import_file_path = import_file.get('resource', None)

                if import_file_path:
                    base_dir = os.path.dirname(file_path).rstrip(os.sep)
                    import_file_path = cls.get_import_file_path(import_file_path=import_file_path, base_dir=base_dir)
                    import_file_data = cls.parse_file_by_path(import_file_path)

                    if import_file_data:
                        yaml_data = cls.merge(import_file_data, yaml_data)

        if 'imports' in yaml_data:
            del yaml_data['imports']

        return yaml_data

    @classmethod
    def inject_parameters(cls, data):
        for key, value in data.items():
            if key in ['services', 'parameters']:
                continue
            if type(value) is not str:
                continue

            injection_regexp = re.compile('^(%[a-zA-Z0-9._]+%)$')
            injection_entries = injection_regexp.findall(value)
            injection_entry = None
            if len(injection_entries):
                injection_entry = injection_entries[0]

            if injection_entry:
                injection_entry_parts = injection_entry.strip('%').split('.')
                parameters = deepcopy(data.get('parameters'))
                for injection_entry_part in injection_entry_parts:
                    if parameters.get(injection_entry_part):
                        parameters = parameters.get(injection_entry_part)
                    else:
                        raise Exception('Parameter `%s` is not defined in parameters section' % (injection_entry))
                data[key] = parameters
        return data

    @classmethod
    def get_import_file_path(cls, import_file_path, base_dir=''):
        import_file_path_regexp = re.compile('^(@[a-zA-Z0-9._]+:)', re.IGNORECASE)
        import_file_module_list = import_file_path_regexp.findall(import_file_path)

        if len(import_file_module_list):
            import_file_module = import_file_module_list[0]
            import_file_path = import_file_path.replace(import_file_module, '')
            import_file_module = import_file_module.replace('@', '').replace(':', '')
            import_file_module = Importer.import_module(import_file_module)
            import_file_path = os.path.dirname(import_file_module.__file__).rstrip(os.sep) + os.sep + import_file_path.strip(os.sep)
        else:
            import_file_path = (base_dir + os.sep if base_dir else '') + (import_file_path.strip(os.sep) if base_dir else import_file_path.rstrip(os.sep))
        return import_file_path


    @classmethod
    def merge(cls, source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                # get node or create one
                node = destination.setdefault(key, {})
                cls.merge(value, node)
            else:
                destination[key] = value
        return destination

    @classmethod
    def save(cls, data, file_path):
        f = open(file_path, 'wb')
        pprinter = pprint.PrettyPrinter(indent=4)
        f.write('# _*_ coding: utf-8 _*_\n\n')
        f.write('from __future__ import unicode_literals\n\n')
        f.write('COMPILED_CONFIG = ')
        f.write(pprinter.pformat(data))
        f.close()


class YamlParser(BaseParser):
    """
    Parsing yaml files and compiling all the services, parameters and configuration into one big config
    """
    @classmethod
    def get_file_contents_as_dict(cls, file_path):
        file_path = cls.get_import_file_path(file_path)
        return load(open(file_path, 'rb'), Loader=Loader)
