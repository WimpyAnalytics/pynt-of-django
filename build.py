#!/usr/bin/python
import os
MODULE_PATH = os.path.abspath(__file__)

# So that we can use our own tools to setup the project as others would
import sys
sys.path.append(os.path.dirname(MODULE_PATH))

import pyntofdjango
pyntofdjango.setup_pod(MODULE_PATH)
from pyntofdjango.tasks import pip, python, clean, create_venv, manage, recreate_venv, runserver, test_tox, migrate, \
    docs, venv_bin, test_manage, delete_venv, dumpdata, test_setup, test_nose

from pyntofdjango import utils
from pynt import task


@task()
def readme_rst():
    """Update README.rst from README.md"""
    utils.execute_python('readme_rst.py')
