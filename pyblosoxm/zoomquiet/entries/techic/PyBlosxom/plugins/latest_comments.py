# -*- coding: utf-8 -*-
#tags techic,PyBlosxom,plugins
"""-最新评注-插件0.5.1
Copyright 2005 Uche Ogbuji.  You may use this work under the
Creative Commons Attribution-ShareAlike 2.0 License.  For details see:

http://creativecommons.org/licenses/by-sa/2.0/

Generates a template variable, $latest_comments, which contains a listing
of the most recent comments to the Weblog, in the form:

<div class="comment-link">
<a href="http://author1url" class="comment-link-author">Author 1</a>
on
<a href="http://entry1url" class="comment-link-entry">Entry 1 title</a>
</div>
<div class="comment-link">
<a href="http://author2url" class="comment-link-author">Author 2</a>
on
<a href="http://entry2url" class="comment-link-entry">Entry 2 title</a>
</div>

Inspired by Burningbird: http://weblog.burningbird.net/

This plugin requires the comments plug-in (comments.py).

This module supports the following, optional config parameter:

    latest_comment_count - the number of comments to include in the
                           output (default 5)
example::
py['latest_comment_count'] = 7

**i18n considerations**

The output uses the blog_encoding variable specified in config.py.  It is
an encoded string set as template variable $latest_comments

**performance considerations**

Stats all comment file each time the blog is fully rendered.  Only opens
the most recent N comment file, where N is the latest_comment_count config
variable, and the blog entry files that correspond to each one.  Reads
(and parses the XML of) the entire contents of each comments file that is
opened.  Only reads the first line of each corresponding blog entry file.
Should not present performance problems unless there are so many comment
files to stat that the user has plenty of other problems, anyway.

If you make any changes to this plugin, please a send a patch with your
changes to uche.ogbuji@gmail.com so that we can incorporate your changes.

up::060124 Zoom.Quiet fixed for new version PyBlosxom tools log
"""

## Leo: tab_width=-4 page_width=80
__author__ = "Uche Ogbuji http://copia.ogbuji.net/blog/"
__version__ = "0.5.1"
__url__ = "http://copia.ogbuji.net/blog/2005-05-16/PyBlosxom_"
__description__ = "Provides a listing of the latest comments on the Weblog"

import glob, os
import bisect
import re, time, os, codecs
import comments

from Pyblosxom import tools
log = tools.getLogger()
def readComment(filename, encoding):
    """
    Read a comment from filename, based on comments.readComment

    @param filename: filename containing a comment
    @type filename: string

    @param encoding: encoding of comment files
    @type encoding: string

    @returns: a comment dict
    """
    from xml.sax import make_parser, SAXException
    from xml.sax.handler import feature_namespaces, ContentHandler
    class cmtHandler(ContentHandler):
        def __init__(self, cmt):
            self._data = ""
            self.cmt = cmt
        def startElement(self, name, atts):
            self._data = ""
        def endElement(self, name):
            self.cmt['cmt_'+name] = self._data
        def characters(self, content):
            self._data += content

    cmt = {}

    try:
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        handler = cmtHandler(cmt)
        parser.setContentHandler(handler)
        parser.parse(filename)
        return cmt
    except: #don't error out on a bad comment
        #tools.log('bad comment file: %s' % filename)
        log.error('bad comment file: %s' % filename)
        return {}
def gather_latest_comments(request):
    config = request.getConfiguration()
    data = request.getData()
    encoding = config['blog_encoding']
    cmt_root = config['comment_dir']
    cmt_ext = config['comment_ext']
    exts = data['extensions']
    count = config['latest_comment_count']
    datadir = config['datadir']
    #lcdir = len(os.path.join(config['datadir'], cmt_root)
    #cmt_summary_maxlen = config['cmt_summary_maxlen']
    encoding = config['blog_encoding']

    enc, dec, read_wrap, write_wrap = codecs.lookup(encoding)
    def entry_from_comment(fname):
        base_path = fname[:fname.rfind('-')]
        if base_path[0] == '/': base_path = base_path[1:]
        full_path = os.path.join(config['datadir'], base_path)
        ext = tools.what_ext(exts, full_path)
        entry_title = ''
        if ext:
            actual_file = full_path+os.path.extsep+ext 
            try:
                f = open(actual_file, 'r')
                entry_title = f.readline()
                #entry_title += " %s"%len(f.readline())
                if "<?xml" in entry_title:
                    entry_title = get2title(f,fname,config['datadir'])
                #entry_title = fname
                f.close()
            except:
                #Can't get title
                #tools.log('Unable to get title for %s'%actual_file)
                log.error('Unable to get title for %s'%actual_file)
        else:
            #tools.log('Unable to get title for %s'%full_path)
            log.error('Unable to get title for %s'%full_path)
        entry_url = config['base_url'] + '/' + base_path
        return entry_title, entry_url


    latest = []
    files = tools.Walk(request
                       , root=cmt_root
                       , recurse=0
                       ,pattern=re.compile('.*\.'+cmt_ext+'$')
                       , return_folders=0)
    for fname in files:
        if fname.endswith('LATEST.'+cmt_ext): continue
        stamp = time.mktime(tools.filestat(request, fname))
        if len(latest) < count:
            entry_title, entry_url = entry_from_comment(fname[len(cmt_root):])
            bisect.insort(latest
                          ,(stamp,fname,entry_title,entry_url))
            continue
        elif stamp > latest[0][0]:
            entry_title, entry_url = entry_from_comment(fname[len(cmt_root):])
            bisect.insort(latest
                          ,(stamp,fname,entry_title,entry_url))
            del latest[0]
    latest.reverse()

    def comment_summary((stamp, filename, entry_title, entry_url)
                        , encoding):
        comment = readComment(filename, encoding)
        summary = u'<div class="comment-link"><a href="mailto:%s" class="comment-link-author">%s</a> :: <a href="%s#blosxomComments" class="comment-link-entry">%s <sup>(%s)c</sup></a></div>'%(
                #dec(comment['cmt_link'])[0]
                dec(comment['cmt_email'])[0]
                , dec(comment['cmt_author'])[0]
                , entry_url
                , dec(entry_title)[0]
                ,len(comment['cmt_description'])
                )
        return summary.encode(encoding)

    latest = [ comment_summary(comment_info
                , encoding) for comment_info in latest ]
    latest = ''.join(latest)

    #tools.log(repr(latest))
    return latest





def get2title(fobj,filename,datadir):
    """esp. for t2t export entry
        - get the <title>content</title> as commtent title
    """
    title = ""
    for line in fobj.readlines():
        if "<title>" in line:
            title=line[8:].replace("</title>","")
            break
    if "" == title:
        title = filename.replace(datadir, '')
    return title

def cb_prepare(args):
    request = args["request"]
    data = request.getData()
    if data.get("entry_list"):
        data["latest_comments"] = gather_latest_comments(request)

