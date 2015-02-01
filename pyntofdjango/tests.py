import unittest
import os
import tempfile
from subprocess import CalledProcessError

import mock

from . import utils
from . import paths


class TestSafeCd(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.temp_dir = tempfile.mkdtemp('pyntofdjango')

    def test_change_yield_revert(self):
        """Safe cd should change directory, yield and revert back"""
        with utils.safe_cd(self.temp_dir):
            os.path.exists(self.temp_dir)

        self.assertEqual(os.getcwd(), self.cwd, "Working directory was not restored.")

    def test_change_error_revert(self):
        """Should restore directory after an exception during yield"""
        try:
            with utils.safe_cd(self.temp_dir):
                raise ValueError
        except ValueError:
            pass

        self.assertEqual(os.getcwd(), self.cwd, "Working directory was not restored.")


class TestExecute(unittest.TestCase):

    @mock.patch('pyntofdjango.utils.check_call')
    @mock.patch('pyntofdjango.utils.print_')
    @mock.patch('pyntofdjango.utils.sys.exit')
    def test_successful_command(self, mock_exit, mock_print_, mock_check_call):
        """A successful command should not exit"""
        utils.execute('python', '-V')

        self.assertFalse(mock_exit.called)
        self.assertFalse(mock_print_.called)
        self.assertTrue(mock_check_call.called)

    @mock.patch('pyntofdjango.utils.check_call')
    @mock.patch('pyntofdjango.utils.print_')
    @mock.patch('pyntofdjango.utils.sys.exit')
    def test_bad_command(self, mock_exit, mock_print_, mock_check_call):
        """A bad command should exit with the error code"""
        command = ['notatall', 'athing']
        mock_check_call.side_effect = CalledProcessError(1, command)

        utils.execute(*command)

        self.assertTrue(mock_exit.called)
        self.assertTrue(mock_print_.called)
        self.assertTrue(mock_check_call.called)


class PathsTestBase(unittest.TestCase):

    paths_under_test = ['root', 'manage_root', 'manage_py', 'local_requirements', 'venv']

    def get_actual_paths(self):
        actual = {}
        for attribute in self.paths_under_test:
            actual[attribute] = getattr(paths.project_paths, attribute)
        return actual

    def get_expected_paths(self):
        expected = {
            'root': self.temp_dir,
            'manage_root': self.temp_dir,
            'manage_py': self.temp_located_manage_py,
            'local_requirements': self.temp_located_requirements,
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
        self.temp_located_requirements = self.temp_local_requirements
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

    def setUp(self):
        self.setup_temp_project()

        paths.project_paths.setup(self.temp_dir, None, None)

    def test_preferred_paths(self):
        """The state the paths should be in with only the required setup and all possible files"""
        self.temp_located_requirements = self.temp_local_requirements

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_test_requirements(self):
        """A test_requirements file should be located when a local_requirements is not present."""
        os.remove(self.temp_local_requirements)
        self.temp_located_requirements = self.temp_test_requirements

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_requirements_local(self):
        """A requirements/local.txt file should be located when a local/test_requirements files are not present."""
        os.remove(self.temp_local_requirements)
        os.remove(self.temp_test_requirements)
        self.temp_located_requirements = self.temp_requirements_local

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_requirements_test(self):
        """A requirements/test.txt should be found when local/test_requirements and local.txt files are not present."""
        os.remove(self.temp_local_requirements)
        os.remove(self.temp_test_requirements)
        os.remove(self.temp_requirements_local)
        self.temp_located_requirements = self.temp_requirements_test

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_requirements_fallback(self):
        """A requirements.txt should be found when no other requirements files are present."""
        os.remove(self.temp_local_requirements)
        os.remove(self.temp_test_requirements)
        os.remove(self.temp_requirements_local)
        os.remove(self.temp_requirements_test)
        self.temp_located_requirements = self.temp_requirements

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)


class TestPathOverrides(PathsTestBase):

    def setUp(self):
        self.setup_temp_project()

    def test_manage_root_override(self):
        """Overriding the manage dir with a valid path"""
        paths.project_paths.setup(self.temp_dir, os.path.dirname(self.temp_manage_py), None)

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_manage_root_invalid_override(self):
        """Overriding the manage dir with an invalid path"""
        try:
            paths.project_paths.setup(self.temp_dir, 'not/a/place', None)
            self.fail('An error should have been raised')
        except ValueError:
            pass

    def test_local_requirements_override(self):
        """Overriding the local requirements with a valid path"""
        paths.project_paths.setup(self.temp_dir, None, self.temp_requirements)
        self.temp_located_requirements = self.temp_requirements

        actual = self.get_actual_paths()
        expected = self.get_expected_paths()

        self.assertDictEqual(expected, actual)

    def test_local_requirements_invalid_override(self):
        """Overriding the local requirements with an invalid path"""
        try:
            paths.project_paths.setup(self.temp_dir, None, 'not/a/file.txt')
            self.fail('An error should have been raised')
        except ValueError:
            pass


class TestPathSizeCheck(PathsTestBase):

    def setUp(self):
        self.setup_temp_project()

    def test_fails_if_larger(self):
        """Should fail if location is larger than expected"""
        try:
            utils.safe_size_check(paths.project_paths.venv, "That's huge!", max_bytes=0)
            self.fail("Check did not fail as we expected.")
        except AssertionError:
            pass