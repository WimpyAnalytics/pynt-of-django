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
                if 'venv' in root:
                    continue
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
                if 'venv' in root:
                    continue
                for requirement_type in requirements_precedence:
                    project_level = '{}_requirements.txt'.format(requirement_type)
                    if project_level in files:
                        self._local_requirements = path.join(root, project_level)
                        return self._local_requirements
                    nested = '{}.txt'.format(requirement_type)
                    if 'requirements' in root and nested in files:
                        self._local_requirements = path.join(root, nested)
                        return self._local_requirements

            if 'requirements.txt' in listdir(self.root): # A last resort
                self._local_requirements = path.join(self.root, 'requirements.txt')
                return self._local_requirements

        return self._check(self._local_requirements, "Local requirements file")

    @property
    def venv(self):
        return path.join(self.root, 'venv')

    def setup(self, root, manage_root, local_requirements):
        if not path.isdir(root):
            raise ValueError("root {} could not be found.".format(root))
        if manage_root and not path.isdir(manage_root):
            raise ValueError("manage_root {} could not be found.".format(manage_root))
        if local_requirements and not path.isfile(local_requirements):
            raise ValueError("local_requirements {} could not be found.".format(local_requirements))
        self._root = root
        self._manage_root = manage_root
        self._local_requirements = local_requirements


project_paths = ProjectPaths()


def setup(build_file_path, manage_dir=None, local_requirements=None):
    global project_paths
    project_paths = ProjectPaths()

    if 'build.py' not in build_file_path or not path.isfile(build_file_path):
        raise ValueError("build_file_path arg should be the path to your build.py. E.g. path.abspath(__file__)")
    root = path.dirname(build_file_path)

    project_paths.setup(root, manage_dir, local_requirements)