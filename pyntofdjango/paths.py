from os import path, walk, listdir


class ProjectPaths(object):

    def __init__(self):
        self._root = None
        self._manage_root = None
        self._local_requirements = None

    def _check(self, value, error_subject):
        if not value:
            raise ValueError("{} not available. You may need to provide it to pyntofdjango.setup.".format(
                error_subject))
        return value

    @property
    def root(self):
        return self._check(self._root, "Location of build.py")

    @property
    def manage_root(self):
        if not self._manage_root:
            # Use the first directory with a manage.py
            for root, dirs, files in walk(self.root):
                if 'manage.py' in files:
                    self._manage_root = root
                    break

        return self._check(self._manage_root, "manage.py dir")

    @property
    def manage_py(self):
        return path.join(self.manage_root, 'manage.py')

    @property
    def local_requirements(self):
        if not self._local_requirements:
            requirements_precedence = ['local', 'test']
            for root, dirs, files in walk(self.root):
                for requirement_type in requirements_precedence:
                    project_level = '{}_requirements.txt'.format(requirement_type)
                    if project_level in files:
                        self._local_requirements = path.join(root, project_level)
                        break
                    nested = '{}.txt'.format(requirement_type)
                    if root == 'requirements' and nested in files:
                        self._local_requirements = path.join(root, nested)
                        break

            if 'requirements.txt' in listdir(self.root): # A last resort
                self._local_requirements = 'requirements.txt'

        return self._check(self._local_requirements, "Local requirements file")

    @property
    def venv(self):
        return path.join(self.root, 'venv')

    @property
    def venv_python(self):
        return path.join(self.venv, 'bin/python')

    @property
    def venv_sphinx(self):
        return path.join(self.venv, 'bin/sphinx-build')

    @property
    def venv_sphinx_auto(self):
        return path.join(self.venv, 'bin/sphinx-autobuild')

    @property
    def venv_pip(self):
        return path.join(self.venv, 'bin/pip')

    def setup(self, root, manage_root, local_requirements):
        self._root = root
        self._manage_root = manage_root
        self._local_requirements = local_requirements


project_paths = ProjectPaths()


def setup(build_file_path, manage_dir=None, local_requirements=None):
    if 'build.py' not in build_file_path or not path.isfile(build_file_path):
        raise ValueError("build_file_path arg should be the path to your build.py. E.g. path.abspath(__file__)")
    root = path.dirname(build_file_path)

    project_paths.setup(root, manage_dir, local_requirements)