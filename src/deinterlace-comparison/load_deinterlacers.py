import os
import sys
import importlib
import inspect
import warnings


def output_func(s):
    print(s)


def load_deinterlace_modules(name, modules_path):

    module_list = name.split('.')
    if name[-1] != '.':
        name += '.'

    sys.path.append(modules_path)

    for m in module_list:
        modules_path = os.path.join(modules_path, m)

    menu_entry_loads = []

    for subdir, dirs, files in os.walk(modules_path):
        if subdir.endswith('__pycache__') or subdir.endswith('ignore'):
            continue

        current_module = name
        subdir = subdir.replace(modules_path, '')

        for d in subdir.split(os.path.sep):
            if d != '' and d != os.path.sep:
                current_module += d + '.'

        for file_name in files:

            module_name = os.path.splitext(file_name)[0]

            if output_func is not None:
                output_func("Searching " + current_module + module_name)

            try:                module = importlib.import_module(current_module + module_name)
            except ImportError as e:
                error_string = f'Could not load {current_module}{module_name}:\n {str(e)}'
                import_errors.append(error_string)
                warnings.warn(error_string)
                continue

            md = module.__dict__
            classes = [v for c, v in md.items() if (isinstance(v, type) and v.__module__ == module.__name__)]

            classes = [v for c, v in md.items() if (isinstance(v, type) and v.__module__ == module.__name__)]

            for clss in classes:
                
                members_list = [v[0] for v in inspect.getmembers(clss)]

                if 'deinterlace' in members_list and 'name' in members_list:

                    menu_entry_loads.append(clss())
                    output_func(f"Usable class: {clss.__name__}")
                else:
                    output_func(f"NOT usable: {clss.__name__}")

    return menu_entry_loads