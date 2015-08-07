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
    Runs a script in the venv bin w/pynt args/kwargs.
    \t\t\t\t    E.g. pynt venv_bin[django-admin.py]
    """
    project.venv_execute(*str_args, **kwargs)


@task()
def pip(*str_args, **kwargs):
    """Runs the project's pip w/pynt args/kwargs"""
    project.execute_pip(*str_args, **kwargs)


@task()
def python(*str_args, **kwargs):
    """Runs the project's python w/pynt args/kwargs"""
    project.execute_python(*str_args, **kwargs)


@task()
def clean(dry_run='n'):
    """Wipes compiled and cached python files. To simulate: pynt clean[dry_run=y]"""
    file_patterns = ['*.pyc', '*.pyo', '*~']
    dir_patterns = ['__pycache__']
    recursive_pattern_delete(project_paths.root, file_patterns, dir_patterns, dry_run=bool(dry_run.lower() == 'y'))


@task()
def delete_venv():
    """Deletes the venv. Uses a max size check for added safety."""
    safe_size_check(project_paths.venv, "Aborting venv removal for safety.")
    execute('rm', '-rf', project_paths.venv)


@task()
def create_venv(local='y', test='y', general='y'):
    """Create virtualenv w/requirements. Specify y/n for local/test/general to control installation."""
    if not path.isdir(project_paths.venv):
        execute('virtualenv', '--distribute', '--no-site-packages', project_paths.venv)
        project.execute_python('-m', 'easy_install', 'pip')
    if local.lower() == 'y' and project_paths.local_requirements:
        project.execute_pip('install', '--upgrade', '-r', project_paths.local_requirements)
    if test.lower() == 'y' and project_paths.test_requirements:
        project.execute_pip('install', '--upgrade', '-r', project_paths.test_requirements)
    if general.lower() == 'y' and project_paths.requirements_txt:
        project.execute_pip('install', '--upgrade', '-r', project_paths.requirements_txt)


@task()
def recreate_venv():
    """Deletes and re creates virtualenv"""
    delete_venv()
    create_venv()


@task()
def manage(*arg_string, **kwargs):
    """Runs the demo's manage.py w/pynt args/kwargs"""
    project.execute_manage(*arg_string, **kwargs)


@task()
def runserver(*args, **kwargs):
    """Runs the demo development server w/pynt args/kwargs"""
    project.execute_manage('runserver', *args, **kwargs)


@task()
def dumpdata(app_target, *args, **kwargs):
    """Dumps data from an app w/pynt args/kwargs. E.g. pynt dumpdata[myapp]"""
    options = {
        '--indent': 4,
    }
    options.update(kwargs)

    # Quiet down pynt...
    logger = logging.getLogger('pynt')
    logger.propagate = False

    project.execute_manage('dumpdata', app_target, *args, **options)


@task()
def test_nose(*args, **kwargs):
    """Runs all tests through nosetests w/pynt args/kwargs"""
    project.venv_execute('nosetests', *args, **kwargs)


@task()
def test_manage(*args, **kwargs):
    """Runs all tests through manage.py w/pynt args/kwargs"""
    with safe_cd(project_paths.manage_root):
        project.execute_manage('test', *args, **kwargs)


@task()
def test_setup(*args, **kwargs):
    """Runs all tests through manage.py w/pynt args/kwargs"""
    project.execute_python('setup.py', 'test', *args, **kwargs)


@task()
def test_tox(*args, **kwargs):
    """Runs all tests for all environments w/pynt args/kwargs. Flush previous with pynt test_tox[flush=y]"""
    args = ['tox'] + list(args)

    # Python 2.7.x does not allow a named arg after variable length args (3 does but we have to support both)
    flush = kwargs.get('flush', 'n')
    if 'flush' in kwargs.keys():
        del kwargs['flush']

    if flush.lower() == 'y':
        args.append('-r')
    execute(*args, **kwargs)


@task()
def migrate(*args, **kwargs):
    """Migrates the development db w/pynt args/kwargs"""
    project.execute_manage('migrate', *args, **kwargs)


@task()
def docs(*args, **kwargs):
    """Makes the docs w/pynt args/kwargs"""
    with safe_cd('docs'):
        project.venv_execute('sphinx-build', '-b', 'html', '.', '_build/html', *args, **kwargs)
