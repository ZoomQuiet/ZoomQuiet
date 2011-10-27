# -*- coding: utf-8 -*-
from Pyblosxom import tools
import os, os.path, posix, re, stat, time

FILETIME = re.compile('^([0-9]{4})-([0-1][0-9])-([0-3][0-9])-([0-2][0-9])-([0-5][0-9]) +(.*)$')

all_timestamps = {}
extensions = []
timestamps_to_save = {}


#mode: python; indent-tabs-mode: t, tab-width: 4 
"""
This allows the user to create a file "timestamps" in their datadir,
that will override the timestamp of any given blog entry. Each line
in this file should be of the form "YYYY-MM-DD-hh-mm file-name".
Then for any entry that one of these lines exist the system will use
that timestamp instead of the actual files modification time.

Note: the filename is relative to your data-dir.
Example of a line for the file /var/data-dir/school/abc.txt
   where the datadir is "/var/data-dir/" and the date is Aug 9, 2004.

2004-08-09-00-00 school/abc.txt
"""
__author__ = 'Nathan Kent Bullock, Ryan Barrett'
__homepage__ = 'http://snarfed.org/space/hardcodedates'
__email__ = 'nathan_kent_bullock -at- yahoo.ca, hardcodedates -at- ryanb.org'
__version__ = '1.4'
def init(request):
    if all_timestamps:
        return  # already initialized

    datadir = request.getConfiguration()['datadir']
    timestamp_file = os.path.join(datadir, 'timestamps')

    if os.path.isfile(timestamp_file):
        f = file(timestamp_file)
        for str in f.readlines():
            m = FILETIME.search(str.strip())
            if m:
                year = int(m.group(1))
                mo = int(m.group(2))
                day = int(m.group(3))
                hr = int(m.group(4))
                minute = int(m.group(5))
                mtime = time.mktime((year,mo,day,hr,minute,0,0,0,-1))
                filename = os.path.join(datadir, m.group(6))
                all_timestamps[filename] = mtime

        f.close()

    extensions.extend(request.getData()['extensions'].keys())
    extensions.append(request.getConfiguration().get('comment_ext', 'cmt'))

def cb_filestat(args):
    request = args['request']
    init(request)

    filename = args['filename']
    extension = os.path.splitext(filename)[1][1:]
    datadir = request.getConfiguration()['datadir']

    if all_timestamps.has_key(filename):
        # we know this file's timestamp
        mtime = args['mtime']
        assert isinstance(mtime, (tuple, posix.stat_result))
        args['mtime'] = (mtime[0:stat.ST_MTIME] + (all_timestamps[filename],) +
                         mtime[stat.ST_MTIME + 1:])

    elif extension in extensions and filename.startswith(datadir):
        # we don't know it, but we should. ask the os for it, and remember it.
        args['mtime'] = os.stat(filename)
        all_timestamps[filename] = args['mtime'][stat.ST_MTIME]
        timestamps_to_save[filename] = args['mtime'][stat.ST_MTIME]

    return args

def cb_end(args):
    if timestamps_to_save:
        datadir = args['request'].getConfiguration()['datadir']
        datadir = os.path.normpath(datadir)
        tsfile = file(os.path.join(datadir, 'timestamps'), 'a')
        for filename, mtime in timestamps_to_save.items():
            time_str = time.strftime('%Y-%m-%d-%H-%M', time.localtime(mtime))
            # strip the datadir prefix and directory separator slash
            filename = filename[len(datadir) + 1:]
            tsfile.write('%s %s\n' % (time_str, filename))
            tools.getLogger().info('Saved mtime %s for %s' % (time_str, filename))
        tsfile.close()
        timestamps_to_save.clear()

