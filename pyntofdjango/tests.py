import unittest
import os
import tempfile
from subprocess import CalledProcessError

import mock
from pyntcontrib import safe_cd, execute

from . import utils
from . import paths


class TestSafeCd(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.temp_dir = tempfile.mkdtemp('pyntofdjango')

    def test_change_yield_revert(self):
        """Safe cd should change directory, yield and revert back"""
        with safe_cd(self.temp_dir):
            os.path.exists(self.temp_dir)

        self.assertEqual(os.getcwd(), self.cwd, "Working directory was not restored.")

    def test_change_error_revert(self):
        """Should restore directory after an exception during yield"""
        try:
            with safe_cd(self.temp_dir):
                raise ValueError
        except ValueError:
            pass

        self.assertEqual(os.getcwd(), self.cwd, "Working directory was not restored.")


class PathsTestBase(unittest.TestCase):

    paths_under_test = [
        'root', 'manage_root', 'manage_py', 'local_requirements', 'test_requirements', 'requirements_txt', 'venv'
    ]
    temp_located_local_requirements = None
    temp_located_test_requirements = None
    temp_located_requirements_txt = None
    project_paths = None

    def get_actual_paths(self):
        actual = {}
        for attribute in self.paths_under_test:
            actual[attribute] = getattr(self.project_paths, attribute)
        return actual

    def get_expected_paths(self):
        expected = {
            'root': self.temp_dir,
            'manage_root': self.temp_dir,
            'manage_py': self.temp_located_manage_py,
            'local_requirements': self.temp_located_local_requirements,
            'test_requirements': self.temp_located_test_requirements,
            'requirements_txt': self.temp_located_requirements_txt,
            'venv': self.temp_venv,
        }
        return expected

    def touch_file(self, file_path):
        with open(file_path, 'a'):
            os.utime(file_path, None)

    def setup_temp_project(self):
        self.temp_dir = tempfile.mkdtemp('pyntofdjango')
        self.temp_manage_py = os.path.join(self.temp_dir, 'manage.py')
        self.temp_local_requirements = os.path.join(self.temp_dir, 'local_requirements.txt')
        self.temp_test_requirements = os.path.join(self.temp_dir, 'test_requirements.txt')
        self.temp_requirements = os.path.join(self.temp_dir, 'requirements.txt')
        self.temp_requirements_dir = os.path.join(self.temp_dir, 'requirements')
        self.temp_requirements_local = os.path.join(self.temp_requirements_dir, 'local.txt')
        self.temp_requirements_test = os.path.join(self.temp_requirements_dir, 'test.txt')
        self.temp_venv = os.path.join(self.temp_dir, 'venv')
        self.temp_venv_sphinx = os.path.join(self.temp_venv, 'bin/sphinx-build')
        self.temp_located_manage_py = self.temp_manage_py
        os.mkdir(self.temp_requirements_dir)
        os.mkdir(self.temp_venv)

        self.touch_file(self.temp_manage_py)
        self.touch_file(self.temp_test_requirements)
        self.touch_file(self.temp_local_requirements)
        self.touch_file(self.temp_requirements_local)
        self.touch_file(self.temp_requirements_test)
        self.touch_file(self.temp_requirements)


class TestNoSetup(PathsTestBase):

    def test_paths(self):
        """No paths should work without setup being called."""
        for attribute in self.paths_under_test:
            try:
                getattr(paths.project_paths, attribute)
                self.fail("Using {} without setup should have raised an error.".format(attribute))
            except ValueError:
                pass


class TestRequiredSetup(PathsTestBase):

    maxDiff = None

    def setUp(self):
        self.setup_temp_project()

        self.project_paths = paths.ProjectPaths()
        self.project_paths.setup(self.temp_dir, None, None)

        self.temp_located_local_requirements = self.temp_local_requirements
        self.temp_located_test_requirements = self.temp_test_requirements
        self.temp_located_requirements_txt = self.temp_requirements

    def _assert_paths(self):
        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_preferred_paths(self):
        """The state the paths should be in with only the required setup and all possible files"""
        self._assert_paths()

    def test_test_requirements_missing(self):
        """A test_requirements file is not at the root."""
        os.remove(self.temp_test_requirements)

        self.temp_located_test_requirements = self.temp_requirements_test

        self._assert_paths()

    def test_requirements_local_missing(self):
        """A requirements/local.txt file should be located when a local_requirements is not at the root."""
        os.remove(self.temp_local_requirements)

        self.temp_located_local_requirements = self.temp_requirements_local

        self._assert_paths()


class TestPathOverrides(PathsTestBase):

    def setUp(self):
        self.setup_temp_project()

        self.temp_located_local_requirements = self.temp_local_requirements
        self.temp_located_test_requirements = self.temp_test_requirements
        self.temp_located_requirements_txt = self.temp_requirements

    def test_manage_root_override(self):
        """Overriding the manage dir with a valid path"""
        self.project_paths = paths.ProjectPaths()
        self.project_paths.setup(self.temp_dir, os.path.dirname(self.temp_manage_py), None)

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_manage_root_invalid_override(self):
        """Overriding the manage dir with an invalid path"""
        try:
            self.project_paths = paths.ProjectPaths()
            self.project_paths.setup(self.temp_dir, 'not/a/place', None)
            self.fail('An error should have been raised')
        except ValueError:
            pass

    def test_local_requirements_override(self):
        """Overriding the local requirements with a valid path"""
        self.project_paths = paths.ProjectPaths()
        self.project_paths.setup(self.temp_dir, None, self.temp_requirements)

        self.temp_located_local_requirements = self.temp_requirements

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_local_requirements_invalid_override(self):
        """Overriding the local requirements with an invalid path"""
        try:
            self.project_paths = paths.ProjectPaths()
            self.project_paths.setup(self.temp_dir, None, 'not/a/file.txt')
            self.fail('An error should have been raised')
        except ValueError:
            pass


class TestPathSizeCheck(PathsTestBase):

    def setUp(self):
        self.setup_temp_project()
        self.project_paths = paths.ProjectPaths()
        self.project_paths.setup(self.temp_dir, None, None)

    def test_fails_if_larger(self):
        """Should fail if location is larger than expected"""
        try:
            utils.safe_size_check(self.project_paths.venv, "That's huge!", max_bytes=0)
            self.fail("Check did not fail as we expected.")
        except AssertionError:
            pass