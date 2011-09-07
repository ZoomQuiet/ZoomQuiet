# -*- coding: utf-8 -*-
"""py - html Parser
    - refactory py.py from xhtml.py

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
PREFORMATTER_ID = 'py'
FILE_EXT = 'py'
__version__ = "v11.08.31"
__author__ = 'Zoom.Quiet <Zoom.Quiet at gmail.com>'
__url__ = "http://blog.zoomquiet.org/pyblosxom/OpenSource/PyBlosxom/plugins/py.html"
__description__ = ".py export hmtl entry with syntaxhighlighter."

from Pyblosxom import tools

def cb_entryparser(args):
    args['py'] = parse
    return args
def parse(filename, request):
    import os, sys
    config = request.getConfiguration()
    print filenames
    source = open(filename,"r").read()
    body = '<pre class="brush: python">%s</pre>' % source
    entry_data = {'body' : body
                 ,'title' : filename.replace(config['datadir'], '')
                 #,'tags' : tags
                 #filename.replace(config['datadir'], '')
                 }
    # Call the postformat callbacks
    tools.run_callback('postformat', {'request': request, 
                                      'entry_data': entry_data})
    return entry_data

