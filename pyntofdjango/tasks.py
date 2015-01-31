from os import path
import logging

from pynt import task

from paths import project_paths
import project
import utils


@task()
def venv_bin(*str_args):
    """
    Runs a script in the venv bin.
    \t\t\t\t    E.g. pynt venv_bin[django-admin.py]
    """
    project.venv_execute(*str_args)


@task()
def pip(*str_args):
    """Runs the project's pip with args"""
    project.execute_pip(*str_args)


@task()
def python(*str_args):
    """Runs the project's python with args"""
    project.execute_python(*str_args)


@task()
def clean():
    """Wipes any compiled python files"""
    utils.execute('find', project_paths.root, '-name', '*.pyc', '-delete')
    utils.execute('find', project_paths.root, '-name', '*.pyo', '-delete')
    utils.execute('find', project_paths.root, '-name', '*~', '-delete')
    utils.execute('find', project_paths.root, '-name', '__pycache__', '-delete')


@task()
def delete_venv():
    """Deletes the virtualenv"""
    utils.execute('rm', '-rf', project_paths.venv)


@task()
def create_venv():
    """Create virtualenv w/local_requirements"""
    if not path.isdir(project_paths.venv):
        utils.execute('virtualenv', '--distribute', project_paths.venv)
        project.execute_python('-m', 'easy_install', 'pip')
    project.execute_pip('install', '--upgrade', '-r', project_paths.local_requirements)


@task()
def recreate_venv():
    """Deletes and re creates virtualenv"""
    delete_venv()
    create_venv()


@task()
def manage(*arg_string):
    """Runs the demo's manage.py with args"""
    project.execute_manage(*arg_string)


@task()
def runserver():
    """Runs the demo development server"""
    project.execute_manage('runserver')


@task()
def dumpdata(app_target):
    """Dumps data from an app"""

    # Quiet down pynt...
    logger = logging.getLogger('pynt')
    logger.propagate = False

    project.execute_manage('dumpdata', '--indent=4', app_target)


@task()
def test_nose():
    """Runs all tests through nosetests"""
    project.venv_execute('nosetests')


@task()
def test_manage():
    """Runs all tests through manage.py"""
    with utils.safe_cd(project_paths.manage_root):
        project.execute_manage('test')


@task()
def test_setup():
    """Runs all tests through manage.py"""
    project.execute_python('setup.py', 'test')


@task()
def test_tox(flush=False):
    """Runs all tests for all environments."""
    args = ['tox']
    if flush:
        args.append('-r')
    utils.execute(*args)


@task()
def migrate():
    """Migrates the development db"""
    project.execute_manage('migrate')


@task()
def docs():
    """Makes the docs"""
    with utils.safe_cd('docs'):
        project.venv_execute('sphinx-build', '-b', 'html', '.', '_build/html')
