# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
from entrodec.component.di.importer import Importer
import pprint

__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'


pprinter = pprint.PrettyPrinter(indent=4)


class Compiler:

    def __init__(self):
        pass

    @classmethod
    def compile(cls, config, output_file_path):
        output_file = open(output_file_path, 'wb')

        output_file.write('# _*_ coding: utf-8 _*_\n')
        output_file.write("# DDN'T CHANGE THIS FILE!\n")
        output_file.write('from __future__ import unicode_literals\n')
        output_file.write('from entrodec.component.di.importer import Importer\n')
        output_file.write('from entrodec.component.config import get_config\n\n')

        for service_name, service_config in config.get('services', dict()).iteritems():
            module_path = service_config.get('module')
            module_object = service_config.get('class')
            module_arguments = service_config.get('arguments')
            class_calls = service_config.get('calls', [])
            allow_constructor = service_config.get('constructor', True)
            is_variable = False
            is_class = True
            is_function = False

            if not module_object:
                module_object = service_config.get('function')
                is_function = True
                is_class = False
                is_variable = False

            if not module_object:
                module_object = service_config.get('variable')
                is_variable = True
                is_function = False
                is_class = False

            class_calls_string = []
            if is_class and class_calls:
                for class_call in class_calls:
                    class_call_method = class_call[0]
                    class_call_params = class_call[1:]
                    class_calls_string.append('    instance.%s(%s)' % (class_call_method, cls.get_module_arguments_string(config=config, module_arguments=class_call_params)))

            class_calls_string = '\n'.join(class_calls_string)

            if module_path and module_object:
                module_instance = Importer.import_module(module_path)
                instance = getattr(module_instance, module_object)

                if not instance:
                    raise Exception('Can not instantiate service: `%s`. Expected function or class.' % (service_name))

                module_arguments_string = cls.get_module_arguments_string(config=config, module_arguments=module_arguments)

                return_instance = '    return instance'
                if is_function:
                    if allow_constructor:
                        return_instance = '    return instance(%s)' % (module_arguments_string if len(module_arguments_string) else '')
                    else:
                        return_instance = '    return instance'
                elif is_class:
                    class_calls_string = '    instance = instance(%s)\n' % (module_arguments_string if len(module_arguments_string) else '') + class_calls_string

                service_getter = [
                    '\ndef get_service_%s_%s():' % (service_name.replace('.', '_'), module_path.replace('.', '_')),
                    '    module_instance = Importer.import_module("%s")' % (module_path),
                    '    instance = getattr(module_instance, "%s")' % (module_object),
                    class_calls_string,
                     return_instance,
                    '\n'
                ]

                output_file.write('\n'.join(service_getter))

        output_file.flush()
        output_file.close()

    @classmethod
    def get_module_arguments_string(cls, config, module_arguments):
        module_arguments_string = []
        if module_arguments:
            if type(module_arguments) is list:
                for argument in module_arguments:
                    service_argument = cls.get_service_argument_call(config=config, argument=argument)
                    if service_argument:
                        argument = service_argument
                    else:
                        argument = pprinter.pformat(argument)
                    module_arguments_string.append('%s' % argument)
                module_arguments_string = ', '.join(module_arguments_string)
            elif type(module_arguments) is dict:
                services_calls = dict()
                for argument_name, argument_value in module_arguments.iteritems():
                    service_argument = cls.get_service_argument_call(config=config, argument=argument_value)
                    if service_argument:
                        services_calls[argument_value] = service_argument
                    module_arguments[argument_name] = argument_value
                module_arguments_string = "**" + str(module_arguments)
                for service_call_search, service_call_replace in services_calls.iteritems():
                    module_arguments_string = module_arguments_string.replace("'" + service_call_search + "'", service_call_replace)
        return module_arguments_string

    @classmethod
    def get_service_argument_call(cls, config, argument):
        if argument.startswith('@SERVICE://'):
            service_name = argument.replace('@SERVICE://', '')
            service = config.get('services', dict()).get(service_name)
            if not service:
                return ''
            module_path = service.get('module')
            return 'get_service_' + service_name.replace('.', '_') + '_' + module_path.replace('.', '_') + '()'
        elif argument.startswith('@CONFIG://'):
            config_name = argument.replace('@CONFIG://', '')
            return 'get_config("' + config_name + '")'