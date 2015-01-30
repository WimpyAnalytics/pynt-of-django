import contextlib
from subprocess import call, check_call, CalledProcessError
import os
import sys

from paths import project_paths


@contextlib.contextmanager
def safe_cd(path):
    """
    Changes to a directory, yields, and changes back.
    Additionally any error will also change the directory back.

    Usage:
    >>> with safe_cd('some/repo'):
    ... call('git status')
    """
    starting_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(starting_directory)


def execute(script, *args):
    """
    Executes a command through the shell. Spaces should breakup the args.

    Usage:
    >>> execute('grep', 'TODO', '*')
    """

    popen_args = [script] + list(args)
    try:
        return check_call(popen_args, shell=False)
    except CalledProcessError as ex:
        print(ex)
        sys.exit(ex.returncode)
    except Exception as ex:
        print('Error: {} with script: {} and args {}'.format(ex, script, args))
        sys.exit(1)


def execute_pip(*args):
    execute(project_paths.venv_pip, *args)


def execute_python(*args):
    execute(project_paths.venv_python, *args)


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