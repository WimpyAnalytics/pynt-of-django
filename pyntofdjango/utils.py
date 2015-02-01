import contextlib
from subprocess import call, CalledProcessError, check_call
import os
import sys

from six import print_


@contextlib.contextmanager
def safe_cd(path):
    """
    Changes to a directory, yields, and changes back.
    Additionally any error will also change the directory back.

    Usage:
    >>> with safe_cd('some/repo'):
    ...     call('git status')
    """
    starting_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(starting_directory)


def execute(script, *args):
    """
    Executes a command through the shell. Spaces should breakup the args.

    Usage:
    >>> execute('grep', 'TODO', '*')
    """

    popen_args = [script] + list(args)
    try:
        return check_call(*popen_args, shell=False)
    except CalledProcessError as ex:
        print_(ex)
        sys.exit(ex.returncode)
    except Exception as ex:
        print_('Error: {} with script: {} and args {}'.format(ex, script, args))
        sys.exit(1)


def safe_size_check(checked_path, error_detail, max_bytes=500000000):
    """Determines if a particular path is larger than expected. Useful before any recursive remove."""
    actual_size = 0
    for dirpath, dirnames, filenames in os.walk(checked_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            actual_size += os.path.getsize(fp)

    assert actual_size <= max_bytes, "Path {} size of {} >= {} bytes. {}".format(
        checked_path, actual_size, max_bytes, error_detail)