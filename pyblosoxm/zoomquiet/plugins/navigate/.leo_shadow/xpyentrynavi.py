#@+leo-ver=4-thin
#@+node:zoomq.20100419111908.3738:@shadow pyentrynavi.py
#@@language python
#@@tabwidth -4
# -*- coding: utf-8 -*-
#@<<declarations>>
#@+node:zoomq.20100419111908.3739:<<declarations>>
"""
Create navigation to the previous/next entry for each entry,
like this.

  < previous entry title | MAIN | next entry title >


To install pyentrynavi, do the following

  1. add "pyentrynavi" to your load_plugins list variable
     in your config.py.
  2. add the $entry_navi variable to your date_head and/or
     comment-story templates.
  3. if your file extension other than "txt", set the following on your
     config.py.

     ex) py["entry_extension"] = "rst"


version 0.4: modified regular expression '(.*\.txt)' to '(.*\.txt$)',
             to prevent hit backup files or swap files.
             Thanks Bill Powell!
version 0.5: modified system depend path handling and enable to use file
             extension other than .txt.
             Thanks Andrey Bondarenko!

----

Copyright (C) 2006-2009 shunuhs

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.

"""

#@-node:zoomq.20100419111908.3739:<<declarations>>
#@nl
__author__      = "shunuhs"
__version__     = "0.5 2009/10/24"
__url1__        = "http://sh1.2-d.jp/b/static/pyentrynavi.html"
__url2__        = "http://sh1.2-d.jp/h/pyblosxom_plugin/file/tip/pyentrynavi.py"
__description__ = "show entry navigator"

from Pyblosxom import tools, entries
import time
import re
import os.path

#@+others
#@+node:zoomq.20100419111908.3740:verify_installation()
def verify_installation(request):
    config = request.getConfiguration()
    if not config.has_key('datadir'):
        print "missing datadir variable"
        return 0
    return 1
#@-node:zoomq.20100419111908.3740:verify_installation()
#@+node:zoomq.20100419111908.3741:cb_prepare()
def cb_prepare(args):
    request = args['request']
    data = request.getData()
    if data['bl_type'] != 'file':
        return

    entry = data['entry_list']
    flavour = data['flavour']
    filename = os.path.normpath(entry[0]['filename']) # normpath is for windows.

    config = request.getConfiguration()
    datadir = config['datadir']
    base_url = config['base_url']

    extension = config.get('entry_extension','txt')

    r = re.compile('(.*\.'+extension+'$)')
    allentries = tools.Walk(request, datadir, pattern=r)

    #    cur_time = time.localtime()

    entrylist = []
    for e in allentries:
        timetuple = tools.filestat(request, e)
#        if cur_time < timetuple:
#            continue

        entrylist.append((timetuple, e))

    entrylist.sort()
    entrylist.reverse()

    entrylist = [x[1] for x in entrylist]
    try:
        num = entrylist.index(filename)
    except ValueError:
        data['entry_navi'] = '| <a href="%s">MAIN</a> |'%base_url
        return

    def _entry_url(file_entry):
      return "%s/%s.%s" % (base_url, file_entry["file_path"], flavour)

    navi_str = ''
    if num != (len(entrylist)-1):
        fname = entrylist[num+1]
        e = entries.fileentry.FileEntry(request, fname, datadir)
        prev_link = _entry_url(e)
        navi_str += '&lt; <a href="%s">%s</a> '%(prev_link,e['title'])

    navi_str += '| <a href="%s">MAIN</a> |'%base_url

    if num:
        fname = entrylist[num-1]
        e = entries.fileentry.FileEntry(request, fname, datadir)
        next_link = _entry_url(e)
        navi_str += ' <a href="%s">%s</a> &gt;'%(next_link,e['title'])

    data['entry_navi'] = navi_str
#@-node:zoomq.20100419111908.3741:cb_prepare()
#@-others



#@-node:zoomq.20100419111908.3738:@shadow pyentrynavi.py
#@-leo
