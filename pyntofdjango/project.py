import os

from paths import project_paths
from utils import execute


def venv_execute(script, *args):
    script_path = os.path.join(project_paths.venv, 'bin', script)
    execute(script_path, *args)


def execute_pip(*args):
    venv_execute('pip', *args)


def execute_python(*args):
    venv_execute('python', *args)


def execute_manage(*args):
    execute_python(project_paths.manage_py, *args)


def recursive_load(search_root):
    """Recursively loads all fixtures"""
    for root, dirs, files in os.walk(search_root):
        dir_name = os.path.basename(root)
        if dir_name == 'fixtures':
            for file_name in files:
                fixture_path = os.path.join(root, file_name)
                execute_manage('loaddata', fixture_path)