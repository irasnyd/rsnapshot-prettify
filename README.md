Introduction
============

This is an addon script for [Rsnapshot](http://rsnapshot.org/) to provide a
much more user-friendly output format. This output format is designed to be a
much closer match to the NetApp style `.snapshot` directories, while being even
more user friendly by providing timestamps in the directory names.

This script can either be run standalone, or integrated with rsnapshot itself
using the `cmd_postexec` configuration option.

Example Usage
=============

Given an input directory structure that looks like this:

    /rsnapshot/hourly.0/machine1.example.com/
    /rsnapshot/hourly.0/machine2.example.com/
    /rsnapshot/hourly.1/machine1.example.com/
    /rsnapshot/hourly.1/machine2.example.com/
    /rsnapshot/hourly.2/machine1.example.com/
    /rsnapshot/hourly.2/machine2.example.com/
    /rsnapshot/hourly.3/machine1.example.com/
    /rsnapshot/hourly.3/machine2.example.com/
    /rsnapshot/hourly.4/machine1.example.com/
    /rsnapshot/hourly.4/machine2.example.com/
    /rsnapshot/hourly.5/machine1.example.com/
    /rsnapshot/hourly.5/machine2.example.com/

    /rsnapshot/daily.0/machine1.example.com/
    /rsnapshot/daily.0/machine2.example.com/
    /rsnapshot/daily.1/machine1.example.com/
    /rsnapshot/daily.1/machine2.example.com/

You can run the script like this:

    $ prettify.py -i /rsnapshot -o /rsnapshot/mount

And you will end up with an output structure of symbolic links, named using the
timestamp of each snapshot:

    /rsnapshot/mount/machine1.example.com/snapshot.2017.01.01T12:00:00 -> /rsnapshot/daily.1/machine1.example.com
    /rsnapshot/mount/machine1.example.com/snapshot.2017.01.02T12:00:00 -> /rsnapshot/daily.0/machine1.example.com
    /rsnapshot/mount/machine1.example.com/snapshot.2017.01.03T00:00:00 -> /rsnapshot/hourly.5/machine1.example.com
    /rsnapshot/mount/machine1.example.com/snapshot.2017.01.03T04:00:00 -> /rsnapshot/hourly.4/machine1.example.com
    /rsnapshot/mount/machine1.example.com/snapshot.2017.01.03T08:00:00 -> /rsnapshot/hourly.3/machine1.example.com
    /rsnapshot/mount/machine1.example.com/snapshot.2017.01.03T12:00:00 -> /rsnapshot/hourly.2/machine1.example.com
    /rsnapshot/mount/machine1.example.com/snapshot.2017.01.03T16:00:00 -> /rsnapshot/hourly.1/machine1.example.com
    /rsnapshot/mount/machine1.example.com/snapshot.2017.01.03T20:00:00 -> /rsnapshot/hourly.0/machine1.example.com

    /rsnapshot/mount/machine2.example.com/snapshot.2017.01.01T12:00:00 -> /rsnapshot/daily.1/machine2.example.com
    /rsnapshot/mount/machine2.example.com/snapshot.2017.01.02T12:00:00 -> /rsnapshot/daily.0/machine2.example.com
    /rsnapshot/mount/machine2.example.com/snapshot.2017.01.03T00:00:00 -> /rsnapshot/hourly.5/machine2.example.com
    /rsnapshot/mount/machine2.example.com/snapshot.2017.01.03T04:00:00 -> /rsnapshot/hourly.4/machine2.example.com
    /rsnapshot/mount/machine2.example.com/snapshot.2017.01.03T08:00:00 -> /rsnapshot/hourly.3/machine2.example.com
    /rsnapshot/mount/machine2.example.com/snapshot.2017.01.03T12:00:00 -> /rsnapshot/hourly.2/machine2.example.com
    /rsnapshot/mount/machine2.example.com/snapshot.2017.01.03T16:00:00 -> /rsnapshot/hourly.1/machine2.example.com
    /rsnapshot/mount/machine2.example.com/snapshot.2017.01.03T20:00:00 -> /rsnapshot/hourly.0/machine2.example.com

This makes it much easier to mount the individual snapshots from a remote
machine over NFS. The improved directory structure also makes this much easier
for users to navigate and understand.
