# -*- coding: utf-8 -*-
"""
category_static.py
    - just fixed for pyblosxom-cmd  staticrender export all .html links
base index.py from:
http://snarfed.org/space/pyblosxom+index
Ryan Barrett <pyblosxom@ryanb.org>
    - Zoom.Quiet 100401

This plugin displays an alphabetical index of all entries. It uses these
optional config variables from config.py, shown here with their defaults:

py['cindex_trigger']            = '/site-index'
py['cindex_num_columns']        = 2
py['cindex_letters_first']      = True
py['cindex_title']              = 'index'
py['cindex_use_story_template'] = True


VERSION:
0.2

TODO:
- use a template instead of hard-coded HTML

Copyright 2006 Ryan Barrett

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""


import math
import os.path
import time
from operator import itemgetter
from Pyblosxom import tools
import Pyblosxom.entries
#import re

__author__ = 'Zoom.Quiet <zoomquiet+pyb at gmail dot com>'
__version__ = '11.09.7'
__url__ = "http://blog.zoomquiet.org/pyblosxom/techic/PyBlosxom/plugins/category_static.html"
__description__ = 'Displays an Category index as Tree for all entries. in one page'
DEFAULT_ROOT = []
def verify_installation(request):
  return 1

def cb_filelist(args):
    request = args['request']
    http = request.getHttp()
    data = request.getData()
    config = request.getConfiguration()
    _baseurl = config.get("base_url", "")

    trigger = config.get('cindex_trigger', 'site-index')
    if http['PATH_INFO'] != trigger:
        return

    # get the entries
    datadir = config['datadir']
    files = tools.Walk(request, datadir)
    files.sort()

    body = '<div id="categoriselist">'
    #print files
    # sort into sections, one for each letter. the dictionary is 
    # letter => (entry name, path) where path is the relative to datadir.
    #sections = {}
    #   the entrise dictionary is 
    # path => (entry name, 0) 
    entrise = []

    entry_extensions = data['extensions'].keys()

    for file in files:
        #objEntry = entries.fileentry.FileEntry(request, file,datadir)
        #print objEntry.keys()  
        assert file.startswith(datadir)
        path, ext = os.path.splitext(file[len(datadir):])
        if ext[1:] in entry_extensions:  # strip the leading period from ext
            entry_name = os.path.basename(path)
            #sections.setdefault(entry_name[0].upper(), []).append((entry_name, path))
            entrise.append((entry_name,path,file))
    #print entrise
    #sortPaths = sorted(entrise.iteritems(), key=itemgetter(1), reverse=True)
    #print sortPaths
    #print _baseurl
    etree = {}
    """{
    "pathID":[(path.split()),"title",...]
    ,
    }
    """
    for entry in entrise:
        e = Pyblosxom.entries.fileentry.FileEntry(request, entry[2], entry[1])
        deeps = entry[1].split("/")[:-1]
        pathID = "".join(deeps)
        if pathID in etree:
            etree[pathID].append((e['title'],entry[1]))
        else:
            etree[pathID]= [tuple(deeps),(e['title'],entry[1])]
    #print etree.keys()
    root_path_list = config.get("category_root_list", DEFAULT_ROOT)
    root_entry_list = []
    for opath in root_path_list:
        #print opath
        crtRoot = []
        for k in etree.keys():
            if opath in k:
                crtRoot.append(k)
        crtRoot.sort()
        root_entry_list.append((opath,crtRoot))

    '''root_entry_list as::
    [('Zen', ['ZenChinese', 'ZenGoogle', 'Zenpythonic']), ('oss', ['oss', 'ossFreeBSD', 'ossMozillaFireFox', 'ossUbuntu']), ('opening', []), ('mind', ['mind']), ('Quiet', ['Quietliving', 'Quietnomeans']), ('utility', ['utilitySubversion', 'utilitySubversionhooks', 'utilitypy4strStructuredText', 'utilitypy4webDjango', 'utilitypy4webMoinMoin', 'utilitypy4webQuixote', 'utilitypy4zh', 'utilityzqlib']), ('internet', ['internet', 'internetFolksonomy']), ('easy', ['easymovie', 'easymusic']), ('techic', ['techic', 'techicEmacs', 'techicPyBlosxom', 'techicPyBlosxomblosxom', 'techicPyBlosxomplugins'])]
    '''
    body += '<h3>/</h3>'
    for e in etree[''][1:]:
        #print "etree[''] include::",e
        body += '<span class="indents">%s</span><a href="%s%s.html">%s</a><br>\n'%(
            "...."
            ,_baseurl
            ,e[1]
            ,e[0]
            )
    #print root_entry_list

    for k in root_entry_list:
        #['techic', 'techicEmacs', 'techicPyBlosxom', 'techicPyBlosxomblosxom', 'techicPyBlosxomplugins']
        body += '<h4>%s/</h4>'%k[0]
        cpath = ""
        for p in k[1]:
            #print etree[p]
            #[('', 'Zen', 'Chinese'), '9.18', 'CC Salon BJ', '\xe2\x80\x9c\xe5\x9b\xbd\xe9\x99\x85\xe8\x87\xaa\xe7\x94\xb1\xe8\xbd\xaf\xe4\xbb\xb6\xe6\x97\xa5\xe2\x80\x9d\xe4\xb9\x8b\xe5\xa4\xb4\xe8\x84\x91\xe9\xa3\x8e\xe6\x9a\xb4', '\xe8\xa1\xa8\xe5\xbd\xa2\xe7\xa0\x81\xe7\x9a\x84\xe6\xb6\x88\xe4\xba\xa1\xe8\x83\x8c\xe6\x99\xaf\xef\xbc\x81']
            epath = "/".join(etree[p][0][2:])
            if k[0] != "".join(etree[p][0]):
                if cpath != epath:
                    cpath = epath
                    ldeep = len(etree[p][0][1:])
                    if 3 > ldeep:
                        body += '<H5>%s/</H5>'%"/".join(etree[p][0][2:])
                    else:
                        body += '<H6>%s/</H6>'%"/".join(etree[p][0][3:])
            for e in etree[p][1:]:
                body += '<span id="%s" class="indents">%s</span><a href="%s%s.html">%s</a><br>\n'%(
                        "/".join(etree[p][0])
                        ,"..."*len(etree[p][0])
                        ,_baseurl
                        ,e[1]
                        ,e[0]
                        )

    '''
    [('', 'easy', 'movie'), '\xe4\xb8\x96\xe9\x97\xb4\xe5\xae\x89\xe5\xbe\x97\xe5\x8f\x8c\xe5\x85\xa8\xe6\xb3\x95,\xe4\xb8\x8d\xe8\xb4\x9f\xe5\xa6\x82\xe6\x9d\xa5\xe4\xb8\x8d\xe8\xb4\x9f\xe5\x8d\xbf!']
    [('', 'easy', 'music'), 'ZARD\xe6\xb6\x88\xe9\x80\x9d\xe4\xba\x86']

    for entry in entrise:
        e = Pyblosxom.entries.fileentry.FileEntry(request, entry[2], entry[1])
        #print e['title']
        #print entry[1].split("/")[:-1]
        body += '<span class="indents">%s</span><a href="%s%s.html">%s</a>%s<br>\n'%(
                "...."*len(entry[1].split("/"))
                ,_baseurl
                ,entry[1]
                ,e['title'] #entry[0]
                ,entry[1]
                )
    '''
    #print body
    body +="</div>" 
    data = {'title': config.get('cindex_title', 'index')}
    # use the epoch for mtime. otherwise, pyblosxom uses the current time, which
    # makes other plugins (like weblogsping) think this is a new entry.
    epoch = time.localtime(0)
    fe = Pyblosxom.entries.base.generate_entry(request, data, body, epoch)
    return [fe]

def cb_story(args):
  request = args['request']
  http = request.getHttp()
  config = request.getConfiguration()
  trigger = config.get('cindex_trigger', 'site-index')

  if (http['PATH_INFO'] == trigger and
      not config.get('cindex_use_story_template', 1)):
    title = config.get('cindex_title', 'index')
    args['template'] = '<h1 class="index">%s</h1>\n<hr />\n$body' % title

  return args
