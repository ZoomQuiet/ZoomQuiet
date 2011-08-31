#######################################################################
# Copyright (c) 2006 Blake Winton
#
# Released into the Public Domain.
#######################################################################

"""
Summary
=======

This plugin implements the ``comment_reject`` callback of the comments
plugin.

If someone tries to comment on an entry that's older than 28 days,
the comment is rejected.


Setup
=====

1. copy this file into your plugins directory
2. add "no_old_comments" to the load_plugins list in your config.py
   file
3. if PyBlosxom is not running as a cgi, then you need to restart
   PyBlosxom


Revisions
=========

1.0 - August 5th 2006: First released.
"""

__author__      = "Blake Winton"
__email__       = "bwinton+blog@latte.ca"
__version__     = "1.0 - August 5th, 2006."
__url__         = "http://example.com/"
__description__ = "Prevent comments on entries older than a month."
__category__    = "comments"
__license__     = "Public Domain"
__registrytags__ = "1.4, 1.5, core"


import sys
import time
from Pyblosxom import tools


def verify_installation(request):
    return 1

def cb_comment_reject(args):
    req = args["request"]
    comment = args["comment"]
    blog_config = req.getConfiguration()

    max_age = blog_config.get('no_old_comments_max_age', 2419200)

    data = req.getData()
    entry = data['entry_list'][0]

    logger = tools.getLogger()

    logger.debug( '%s -> %s' % (entry['mtime'], comment) )
    
    if ( (time.time() - entry['mtime']) >= max_age):
        logger.info('Entry too old, comment not posted!')
        return 1

    logger.info('Entry ok, comment posted!')
    return 0
