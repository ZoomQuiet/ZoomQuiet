"""
Summary
=======

Walks through all your blog entries and comments and makes a list of
all the entries that were either written in the last 14 days or have
comments written in the last 14 days.  It then generates a very
hard-coded html representation of them and semi-abuses the 
flavour template yearmonthsummary which I use for my wbgarchives
plugin.

This plugin requires no installation.  Just drop it in and the url
will be::

   $baseurl/recent

to see the recent activity.

----

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright 2004-2007 Will Guaraldi

SUBVERSION VERSION: $Id$

Revisions:
2007-07-07 - Converted documentation to reST.
2005-11-11 - Pulled into new VCS.
1.5 - (26 October, 2005) pulled into new VCS
1.1 - (09 December, 2004) fixed the timestamp and date_head issues
1.0 - (31 August, 2004) initial writing
"""
__author__ = "Will Guaraldi - willg at bluesock dot org"
__version__ = "$Date$"
__url__ = "http://www.bluesock.org/~willg/pyblosxom/"
__description__ = "Summary of recent blog activity."

from Pyblosxom import tools, entries
import time, os, glob, urllib

def verify_installation(request):
    return 1


def new_entry(request, title, body):
    """
    Takes a bunch of variables and generates an entry out of it.  It creates
    a timestamp so that conditionalhttp can handle it without getting
    all fussy.
    """
    entry = entries.base.EntryBase(request)

    entry['title'] = title
    entry['filename'] = title + "/recent"
    entry['file_path'] = title
    entry._id = title + "::recent"

    entry["template_name"] = "yearsummarystory"
    entry["nocomments"] = "yes"

    entry.setTime(time.localtime())
    entry.setData(body)

    return entry


INIT_KEY = "wbgrecent_initiated"

def cb_date_head(args):
    request = args["request"]
    data = request.getData()

    if data.has_key(INIT_KEY):
        args["template"] = ""
    return args

def get_comment_text(cmt):
    f = open(cmt[1], "r")
    lines = f.readlines()
    title = "No title"
    author = "Unknown"
    for mem in lines:
        mem = mem.rstrip()
        if mem.find("<title>") == 0:
            title = mem.replace("<title>", "").replace("</title>", "")
            title = urllib.unquote(title)
        elif mem.find("<author>") == 0:
            author = mem.replace("<author>", "").replace("</author>", "")
            author = urllib.unquote(author)

    return "(%s) comment from %s" % \
           (time.strftime("%m/%d/%Y %H:%M", time.localtime(cmt[0])), \
            author)

def cb_filelist(args):
    request = args["request"]
    pyhttp = request.getHttp()
    data = request.getData()
    config = request.getConfiguration()

    if not pyhttp["PATH_INFO"].startswith("/recent"):
        return

    datadir = config["datadir"]
    baseurl = config.get("base_url", "")
    cmntdir = config.get("comment_dir", datadir + os.sep + "comments")
    cmntext = config.get("comment_ext", ".cmt")

    data["blog_title"] = config.get("blog_title", "") + " - recent activity"
    data[INIT_KEY] = 1
    config['num_entries'] = 9999

    marker = time.time() - (60 * 60 * 24 * 14)

    # get all the entries
    allentries = tools.Walk(request, datadir)

    debug = []
    stuff = []

    for mem in allentries:
        timetuple = tools.filestat(request, mem)
        entrytstamp = time.mktime(timetuple)
        tstamp = entrytstamp

        absolute_path = mem[len(datadir):mem.rfind(os.sep)]
        fn = mem[mem.rfind(os.sep)+1:mem.rfind(".")]

        cmtexpr = os.path.join(cmntdir + absolute_path, fn + '-*.' + cmntext)
        cmtlist = glob.glob(cmtexpr)
        cmtlist = [ (os.stat(m)[8], m) for m in cmtlist]
        cmtlist.sort()
        cmtlist.reverse()

        # we want the most recent mtime from either the entry or
        # any of its comments
        if len(cmtlist) > 0:
            if tstamp < cmtlist[0][0]:
                tstamp = cmtlist[0][0]

        # if the mtime is more recent than our marker, we toss the
        # stuff into our list of things to look at.
        if tstamp > marker:
            stuff.append( [tstamp, entrytstamp, mem, cmtlist] )


    stuff.sort()
    stuff.reverse()

    # time stamp and blog entry
    e = "<tr>\n<td valign=\"top\" align=\"left\">%s:</td>\n" \
        "<td><a href=\"%s/%s\">%s</a> (%s)<br />%s</td></tr>\n"

    entrylist = []
    output = []
    for mem in stuff:
        entry = entries.fileentry.FileEntry(request, mem[2], config["datadir"])
        tstamp = time.strftime("%m/%d/%Y", time.localtime(mem[1]))

        temp = e % (tstamp, \
                    baseurl, \
                    entry["file_path"], \
                    entry["title"], \
                    entry["path"], \
                    "".join( [get_comment_text(c) + "<br />" for c in mem[3]]))
        output.append(temp)

    entrylist.append(new_entry(request, "Recent activity:", "<tr><td colspan=2>&nbsp;</td></tr>\n".join(output)))

    return entrylist
