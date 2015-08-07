import fnmatch
import os
import shutil

from six import print_
from pyntcontrib import execute as _execute


# TODO: Remove this when pyntcontrib's execute does this
def _kwargs_to_execute_args(kwargs):
    args = ['='.join([str(key), str(value)]) for key, value in kwargs.items()]
    return args


def safe_size_check(checked_path, error_detail, max_bytes=500000000):
    """Determines if a particular path is larger than expected. Useful before any recursive remove."""
    actual_size = 0
    for dirpath, dirnames, filenames in os.walk(checked_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            actual_size += os.path.getsize(fp)

    assert actual_size <= max_bytes, "Path {} size of {} >= {} bytes. {}".format(
        checked_path, actual_size, max_bytes, error_detail)


def recursive_pattern_delete(root, file_patterns, directory_patterns, dry_run=False):
    """Recursively deletes files matching a list of patterns. Same for directories"""
    for root, dirs, files in os.walk(root):
        for pattern in file_patterns:
            for file_name in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, file_name)
                if dry_run:
                    print_('Removing {}'.format(file_path))
                    continue
                os.remove(file_path)

        for pattern in directory_patterns:
            for found_dir in fnmatch.filter(dirs, pattern):
                if os.path.exists(found_dir):
                    if dry_run:
                        print('Removing directory tree {}'.format(found_dir))
                        continue
                    shutil.rmtree(found_dir)


def execute(*args, **kwargs):
    """A wrapper of pyntcontrib's execute that handles kwargs"""
    if kwargs:
        # TODO: Remove this when pyntcontrib's execute does this
        args = list(args)
        args.extend(_kwargs_to_execute_args(kwargs))
    _execute(*args)
