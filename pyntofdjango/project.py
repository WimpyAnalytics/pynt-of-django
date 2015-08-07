import os

from .paths import project_paths
from .utils import execute


def venv_execute(script, *args, **kwargs):
    script_path = os.path.join(project_paths.venv, 'bin', script)
    execute(script_path, *args, **kwargs)


def execute_pip(*args, **kwargs):
    venv_execute('pip', *args, **kwargs)


def execute_python(*args, **kwargs):
    venv_execute('python', *args, **kwargs)


def execute_manage(*args, **kwargs):
    execute_python(project_paths.manage_py, *args, **kwargs)


def recursive_load(search_root):
    """Recursively loads all fixtures"""
    for root, dirs, files in os.walk(search_root):
        dir_name = os.path.basename(root)
        if dir_name == 'fixtures':
            for file_name in files:
                fixture_path = os.path.join(root, file_name)
                execute_manage('loaddata', fixture_path)