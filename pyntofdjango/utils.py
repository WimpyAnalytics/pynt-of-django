import contextlib
from subprocess import call, check_call, CalledProcessError
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
        return check_call(popen_args, shell=False)
    except CalledProcessError as ex:
        print_(ex)
        sys.exit(ex.returncode)
    except Exception as ex:
        print_('Error: {} with script: {} and args {}'.format(ex, script, args))
        sys.exit(1)