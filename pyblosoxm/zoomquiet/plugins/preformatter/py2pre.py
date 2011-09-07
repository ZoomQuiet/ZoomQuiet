# -*- coding: utf-8 -*-
"""py - html Parser
    - refactory py2pre.py from xhtml.py

Copyright (c) 2011 Zoom.Quiet 
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by the zoomquiet.org.  The name of the
University may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


"""


## Leo: tab_width=-4 page_width=80
__version__ = "v11.09.7"
__author__ = 'Zoom.Quiet <zoomquiet+pyb at gmail dot com>'
__url__ = "http://blog.zoomquiet.org/pyblosxom/techic/PyBlosxom/plugins/py2pre.html"
__description__ = ".py export hmtl entry with syntaxhighlighter."

#from Pyblosxom import tools

def cb_entryparser(entryparsingdict):
    """
    Register self as plain file handler
    """
    entryparsingdict["py"] = parse
    return entryparsingdict
def parse(filename, request):
    #import os
    entrydata = {}
    source = open(filename, "r").read()
    #print filenames
    body = '<pre class="brush: python">%s</pre>' % source
    entrydata = {'body' : body
                 ,'title' : filename.split("/")[-1]
                 }
    return entrydata

