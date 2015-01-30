from os import path

ROOT = path.dirname(path.abspath(path.join(__file__, '../')))
DEMO_ROOT = path.join(ROOT, 'demo')
VIRTUALENV = path.join(ROOT, 'venv')
VENV_PYTHON = path.join(VIRTUALENV, 'bin/python')
VENV_SPHINX = path.join(VIRTUALENV, 'bin/sphinx-build')
VENV_SPHINX_AUTO = path.join(VIRTUALENV, 'bin/sphinx-autobuild')
PIP = path.join(VIRTUALENV, 'bin/pip')
LOCAL_REQUIREMENTS = path.join(ROOT, 'local_requirements.txt')
DEMO_MANAGE_PY = path.join(DEMO_ROOT, 'manage.py')
