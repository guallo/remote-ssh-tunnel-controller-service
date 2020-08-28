import os
import re
import signal
import importlib

from . import config


def import_modules(dir_path, package_name=None):
    file_name_pattern = re.compile(r'^(?P<module_name>p(?P<module_priority>[0-9][0-9])_.+)\.py$')
    modules = []
    
    with os.scandir(dir_path) as it:
        for entry in it:
            if not entry.is_file():
                continue
            
            match = re.search(file_name_pattern, entry.name)
            
            if not match:
                continue
            
            modules.append((int(match['module_priority']), match['module_name']))
    
    modules.sort()
    
    for module_priority, module_name in modules:
        importlib.import_module(f'{module_name}' if package_name is None 
                            else f'{package_name}.{module_name}')


def import_configd():
    import_modules(config.CONFIGD_PACKAGE_DIRECTORY, os.path.basename(config.CONFIGD_PACKAGE_DIRECTORY))


def import_addons():
    import_modules(config.ADDONS_PACKAGE_DIRECTORY, os.path.basename(config.ADDONS_PACKAGE_DIRECTORY))


def timeout(seconds, callable_, *args, **kwargs):
    def alarm_handler(signum, frame):
        raise TimeoutError('Timed out.')
    
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(seconds)
    
    try:
        return callable_(*args, **kwargs)
    finally:
        signal.alarm(0)
