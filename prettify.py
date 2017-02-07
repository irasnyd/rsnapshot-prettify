#!/usr/bin/env python

'''
Extra script for rsnapshot to make beautifully arranged backup directories
which users can navigate much more easily than in the default scheme
'''

import argparse
import datetime
import sys
import os

def abspath(path):
    '''Wrapper to make it easy to get absolute paths'''
    return os.path.abspath(os.path.realpath(path))

def mkdir_p(directory):
    '''Wrapper around os.makedirs() that ignores existing directories'''
    try:
        os.makedirs(directory)
    except OSError, ex:
        # ignore errno 17 "File exists"
        if ex.errno != 17:
            raise

def symlink(src, dst):
    '''Wrapper around os.symlink() that fixes up any errors automatically'''
    try:
        os.symlink(src, dst)
    except OSError, ex:
        # re-raise on unknown exception
        if ex.errno != 17:
            raise

        # automatically fix up errno 17 "File exists" in an atomic
        # manner using rename (which is atomic in POSIX)
        newdst = dst + '.new'

        if os.path.exists(newdst):
            os.unlink(newdst)

        os.symlink(src, newdst)
        os.rename(newdst, dst)

def listdir(directory):
    '''Wrapper around os.listdir() that ignores non-existent directories'''
    try:
        return sorted(os.listdir(directory))
    except OSError, ex:
        # return empty list on errno 2 "No such file or directory"
        if ex.errno == 2:
            return []

        # otherwise, re-raise the exception
        raise

def pretty_name_from_path(args, path):
    '''
    Calculate a "pretty" name from the absolute path to a rsnapshot
    backup directory.

    Example Input: /data/rsnapshot/hourly.0/host1.example.com/
    Example Output: /data/rsnapshot/mounts/host1.example.com/snapshot.2017-01-02T03:04:05/
    '''
    components = os.path.realpath(path).split(os.sep)
    backup_name = components[-1]

    snapshot_ctime = os.path.getctime(path)

    output_name = datetime.datetime.fromtimestamp(snapshot_ctime).strftime(r'snapshot.%FT%T')
    output_path = os.path.join(args.output_directory, backup_name, output_name)

    return output_path

def symlink_is_up_to_date(src, dst):
    '''Check to see if a symlink already exists and has the expected target'''
    # ignore things which are not symbolic links
    if not os.path.islink(src):
        return True

    # get symlink target
    target_path = os.readlink(src)

    # both the actual and expected target must match
    return target_path == dst

def prettify(args):
    '''Actually perform the prettification of the rsnapshot directory structure'''
    # get each snapshot name: hourly.0, hourly.1, ..., daily.0, ...
    for snapshot_name in listdir(args.input_directory):
        # calculate the full path to the snapshot
        snapshot_path = abspath(os.path.join(args.input_directory, snapshot_name))

        # skip the output directory if they are colocated
        if snapshot_path == args.output_directory:
            continue

        # get each backup name within the snapshot (usually each hostname backed up)
        for backup_name in listdir(snapshot_path):
            # calculate the full path to the backup
            backup_path = abspath(os.path.join(snapshot_path, backup_name))

            output_path = pretty_name_from_path(args, backup_path)

            # skip link creation if the symlink already exists and is up to date
            if symlink_is_up_to_date(backup_path, output_path):
                continue

            # create the directory and symlink it
            if args.dry_run:
                print 'mkdir -p', os.path.dirname(output_path)
                print 'ln -s %s %s' % (backup_path, output_path)
            else:
                mkdir_p(os.path.dirname(output_path))
                symlink(backup_path, output_path)

    # cleanup output directory
    for symlink_name in listdir(args.output_directory):
        symlink_path = abspath(os.path.join(args.output_directory, symlink_name))

        # skip things which are not symbolic links
        if not os.path.islink(symlink_path):
            continue

        # get symlink target
        target_path = os.readlink(symlink_path)

        # calculate expected symlink name
        output_path = pretty_name_from_path(args, target_path)

        # if the symlink target and the expected target match,
        # then this is up to date and we can skip it
        if symlink_path == output_path:
            continue

        # they are out of date, we need to unlink
        if args.dry_run:
            print 'rm', symlink_path
        else:
            os.unlink(symlink_path)

def main():
    '''Main entrypoint'''
    description = 'Improve user-friendliness of rsnapshot directory format using symlinks'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-n', '--dry-run', action='store_true', help='Do not perform any action (test mode)')
    parser.add_argument('-i', '--input-directory', '--snapshot-root', required=True, help='Rsnapshot snapshot_root directory')
    parser.add_argument('-o', '--output-directory', required=True, help='Output directory for symlinks')
    args = parser.parse_args()

    # make sure to use absolute paths, it makes the rest of the code easier
    args.input_directory = abspath(args.input_directory)
    args.output_directory = abspath(args.output_directory)

    prettify(args)
    sys.exit(0)

if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et tw=112: