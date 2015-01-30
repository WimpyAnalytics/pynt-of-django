#!/usr/bin/python
import os
MODULE_PATH = os.path.abspath(__file__)

# So that we can use our own tools to setup the project as others would
import sys
sys.path.append(os.path.dirname(MODULE_PATH))

import pyntofdjango
pyntofdjango.setup(MODULE_PATH)
from pyntofdjango.tasks import pip, python, clean, create_venv, manage, recreate_venv, runserver, tests_tox, migrate, \
    docs, venv_bin

from pyntofdjango import utils
from pynt import task


@task()
def readme_rst():
    """Update README.rst from README.md"""
    utils.execute_python('readme_rst.py')
