from os import path
import logging

from pynt import task

from paths import project_paths
import utils


@task()
def pip(*str_args):
    """Runs the project's pip with args"""
    utils.execute_pip(*str_args)


@task()
def python(*str_args):
    """Runs the project's python with args"""
    utils.execute_python(*str_args)


@task()
def clean():
    """Wipes any compiled python files"""
    utils.execute('find {} -name "*.pyc" -delete'.format(project_paths.root))
    utils.execute('find {} -name "*.pyo" -delete'.format(project_paths.root))
    utils.execute('find {} -name "*~" -delete'.format(project_paths.root))
    utils.execute('find {} -name "__pycache__" -delete'.format(project_paths.root))


@task()
def delete_venv():
    """Deletes the virtualenv"""
    utils.execute('rm', '-rf', project_paths.venv)


@task()
def create_venv():
    """Create virtualenv w/local_requirements"""
    if not path.isdir(project_paths.venv):
        utils.execute('virtualenv', '--distribute', project_paths.venv)
        utils.execute_python('-m', 'easy_install', 'pip')
    utils.execute_pip('install', '--upgrade', '-r', project_paths.local_requirements)


@task()
def recreate_venv():
    """Deletes and re creates virtualenv"""
    delete_venv()
    create_venv()


@task()
def manage(*arg_string):
    """Runs the demo's manage.py with args"""
    utils.execute_manage(*arg_string)


@task()
def runserver():
    """Runs the demo development server"""
    utils.execute_manage('runserver')


@task()
def dumpdata(app_target):
    """Dumps data from an app"""

    # Quiet down pynt...
    logger = logging.getLogger('pynt')
    logger.propagate = False

    utils.execute_manage('dumpdata', '--indent=4', app_target)


@task()
def tests_manage():
    """Runs all tests through manage.py"""
    with utils.safe_cd(project_paths.manage_root):
        utils.execute_manage('test')


@task()
def tests_tox(flush=False):
    """Runs all tests for all environments."""
    args = ['tox']
    if flush:
        args.append('-r')
    utils.execute(*args)


@task()
def migrate():
    """Migrates the development db"""
    utils.execute_manage('migrate')


@task()
def docs():
    """Makes the docs"""
    with utils.safe_cd('docs'):
        utils.execute(project_paths.venv_sphinx, '-b', 'html', '.', '_build/html')


@task()
def rundocserver():
    """Runs the sphinx-autobuild server"""
    with utils.safe_cd('docs'):
        utils.execute(project_paths.venv_sphinx_auto, '.', '_build/html')