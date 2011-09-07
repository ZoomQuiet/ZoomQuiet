# -*- coding: utf-8 -*-
"""
A reStructuredText entry formatter for pyblosxom.  reStructuredText is 
part of the docutils project (http://docutils.sourceforge.net/).  To 
use, you need a *recent* version of docutils.  A development snapshot 
(http://docutils.sourceforge.net/#development-snapshots) will work fine.  

Install docutils, copy this file to your pyblosxom Pyblosxom/plugins
directory, and you're ready to go.  Files with a .rst extension will be
marked up as reStructuredText. 

You can configure this as your default preformatter for .t2t files by
configuring it in your config file as follows::

    py['parser'] = 'txt2tags'

or in your blosxom .txt file entries, place a '#parser txt2tags' line after the
title of your blog::

    My Little Blog Entry
    #parser txt2tags
    My main story...

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

Copyright 2003, 2004, 2005 Sean Bowman
"""



## Leo: tab_width=-4 page_width=80
PREFORMATTER_ID = 'txt2tags'
FILE_EXT = 't2t'
__version__ = '$Id$'
__author__ = 'Zoom.Quiet <Zoom dot Quiet  at gmail.com>'
T2T = "/usr/local/bin/txt2tags"

from Pyblosxom import tools
def cb_entryparser(args):
    args['t2t'] = parse
    #args[FILE_EXT] = readfile
    return args


def parse(filename, request):
    import os, sys    
    config = request.getConfiguration()

    act = T2T+" -t html --toc -o - %s"%filename

    html = os.popen(act).read().strip()
    #html += act
    print act

    entryData = {'body' : html,
                 'title' : filename.replace(config['datadir'], '')}
    return entryData



