from . import paths


def setup_pod(build_file_path, manage_dir=None, local_requirements=None):
    """
    This must be called by the project's build.py for pyntofdjango to function.


    You can specify it directly with the optional manage_dir kwarg.

    :param build_file_path: E.g. os.path.abspath(__file__)
    :param manage_dir: Optional, Searched for if None.
    :param local_requirements: Optional, pip requirements file for local development. Searched for if None.
    :return:
    """
    paths.setup(build_file_path, manage_dir=manage_dir, local_requirements=local_requirements)
