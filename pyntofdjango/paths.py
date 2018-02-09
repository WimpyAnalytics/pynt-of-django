from os import path, walk, listdir


class ProjectPaths(object):

    def __init__(self):
        self._root = None
        self._manage_root = None
        self._local_requirements = None
        self._test_requirements = None
        self._requirements_txt = None

    def _check(self, value, error_subject):
        if not value:
            raise ValueError("{} not available. You may need to provide it to pyntofdjango.setup.".format(
                error_subject))
        return value

    def _locate_specific_requirements(self, specific_part, dest_attr):
        for root, dirs, files in walk(self.root):
            if 'venv' in root:
                continue

            project_level = '{}_requirements.txt'.format(specific_part)
            if project_level in files:
                full_path = path.join(root, project_level)
                setattr(self, dest_attr, full_path)
                return full_path

            nested = '{}.txt'.format(specific_part)
            if 'requirements' in root and nested in files:
                full_path = path.join(root, nested)
                setattr(self, dest_attr, full_path)
                return full_path

    @property
    def root(self):
        return self._check(self._root, "Location of build.py")

    @property
    def manage_root(self):
        if not self._manage_root:
            # Use the first directory with a manage.py
            for root, dirs, files in walk(self.root):
                if 'venv' in root or '.tox' in root:
                    continue
                if 'manage.py' in files:
                    self._manage_root = root
                    break

        return self._check(self._manage_root, "manage.py dir")

    @property
    def manage_py(self):
        return path.join(self.manage_root, 'manage.py')

    @property
    def test_requirements(self):
        if not self._test_requirements:
            self._locate_specific_requirements('test', '_test_requirements')
        return self._test_requirements

    @property
    def requirements_txt(self):
        if not self._requirements_txt:
            name = 'requirements.txt'
            for root, dirs, files in walk(self.root):
                if 'venv' in root:
                    continue

                if name in files:
                    self._requirements_txt = path.join(root, name)
                    return self._requirements_txt
        return self._requirements_txt

    @property
    def local_requirements(self):
        if not self._local_requirements:
            self._locate_specific_requirements('local', '_local_requirements')
        return self._local_requirements

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