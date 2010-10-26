# -*- coding: utf-8 -*-
#tags techic,PyBlosxom,plugins
"""XHTML - html Parser
    - 仅仅适用于 t2t 输出的xhtml

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

Copyleft 2005, 2006 Zoom.Quiet

"""


## Leo: tab_width=-4 page_width=80
PREFORMATTER_ID = 'xhtml'
FILE_EXT = 'xhtml'
__version__ = "v10.4.14"
__author__ = 'Zoom.Quiet <Zoom.Quiet at gmail.com>'
__url__ = "http://blog.zoomquiet.org/pyblosxom/OpenSource/PyBlosxom/plugins/xhtml.phtm"
__description__ = "txt2tags export xhmtl entry - Pyblosxom Parser."

from Pyblosxom import tools

def cb_entryparser(args):
    args['xhtml'] = parse
    return args
def parse(filename, request):
    import os, sys
    config = request.getConfiguration()
    ## 简单处理,基于 t2t 2.4.3
    source = open(filename,"r").readlines()
    body = "".join(source[11:-1])
    title = source[6][7:-9]
    '''
    title = ""
    for line in open(filename,"r").readlines():
        if "<title>" in line:
            title=line[7:].replace("</title>","")
            break
    if "" == title:
        title = filename.replace(config['datadir'], '')
    '''
    entryData = {'body' : body
                 ,'title' : title
                 #filename.replace(config['datadir'], '')
                 }

    return entryData

