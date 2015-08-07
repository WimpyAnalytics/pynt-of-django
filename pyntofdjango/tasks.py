from os import path
import logging

from pynt import task

from .paths import project_paths
from . import project
from .utils import safe_size_check, recursive_pattern_delete
from pyntcontrib import execute, safe_cd


@task()
def venv_bin(*str_args, **kwargs):
    """
    Runs a script in the venv bin.
    \t\t\t\t    E.g. pynt venv_bin[django-admin.py]
    """
    project.venv_execute(*str_args, **kwargs)


@task()
def pip(*str_args, **kwargs):
    """Runs the project's pip with args"""
    project.execute_pip(*str_args, **kwargs)


@task()
def python(*str_args, **kwargs):
    """Runs the project's python with args"""
    project.execute_python(*str_args, **kwargs)


@task()
def clean(dry_run=None):
    """Wipes compiled and cached python files"""
    file_patterns = ['*.pyc', '*.pyo', '*~']
    dir_patterns = ['__pycache__']
    recursive_pattern_delete(project_paths.root, file_patterns, dir_patterns, dry_run=bool(dry_run))


@task()
def delete_venv():
    """Deletes the venv with a max size check."""
    safe_size_check(project_paths.venv, "Aborting venv removal for safety.")
    execute('rm', '-rf', project_paths.venv)


@task()
def create_venv():
    """Create virtualenv w/local_requirements"""
    if not path.isdir(project_paths.venv):
        execute('virtualenv', '--distribute', project_paths.venv)
        project.execute_python('-m', 'easy_install', 'pip')
    project.execute_pip('install', '--upgrade', '-r', project_paths.local_requirements)
    project.execute_pip('install', '--upgrade', '-r', project_paths.test_requirements)


@task()
def recreate_venv():
    """Deletes and re creates virtualenv"""
    delete_venv()
    create_venv()


@task()
def manage(*arg_string, **kwargs):
    """Runs the demo's manage.py with args"""
    project.execute_manage(*arg_string, **kwargs)


@task()
def runserver(*args, **kwargs):
    """Runs the demo development server"""
    project.execute_manage('runserver', *args, **kwargs)


@task()
def dumpdata(app_target, **kwargs):
    """Dumps data from an app"""
    options = {
        '--indent': 4,
    }
    options.update(kwargs)

    # Quiet down pynt...
    logger = logging.getLogger('pynt')
    logger.propagate = False

    project.execute_manage('dumpdata', app_target, **options)


@task()
def test_nose(*args, **kwargs):
    """Runs all tests through nosetests"""
    project.venv_execute('nosetests', *args, **kwargs)


@task()
def test_manage(*args, **kwargs):
    """Runs all tests through manage.py"""
    with safe_cd(project_paths.manage_root):
        project.execute_manage('test', *args, **kwargs)


@task()
def test_setup(*args, **kwargs):
    """Runs all tests through manage.py"""
    project.execute_python('setup.py', 'test', *args, **kwargs)


@task()
def test_tox(flush=False, *args, **kwargs):
    """Runs all tests for all environments."""
    args = [arg for arg in args] + ['tox']
    if flush:
        args.append('-r')
    execute(*args, **kwargs)


@task()
def migrate(*args, **kwargs):
    """Migrates the development db"""
    project.execute_manage('migrate', *args, **kwargs)


@task()
def docs(*args, **kwargs):
    """Makes the docs"""
    with safe_cd('docs'):
        project.venv_execute('sphinx-build', '-b', 'html', '.', '_build/html', *args, **kwargs)
