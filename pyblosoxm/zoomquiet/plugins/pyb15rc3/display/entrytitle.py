#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

If PyBlosxom is rendering a single entry (i.e. entry_list has 1 item
in it), then this populates the ``entry_title`` variable for the
header template.

Usage
=====

To use, add the ``$entry_title`` variable to your header template in
the <title> area.

Example::

    <title>$(blog_title)$(entry_title)</title>

The default $(entry_title) starts with a :: and ends with the title of
the entry.  For example::

    :: Guess what happened today

You can set the entry title template in the configuration properties
with the ``entry_title_template`` variable.

    config["entry_title_template"] = ":: %(title)s"

The ``%(title)s`` is a Python string formatter that gets filled in with
the entry title.
"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2010-04-14"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "Populates $(entry_title) for head template."
__category__ = "date"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


def verify_installation(request):
    return 1

def cb_head(args):
    req = args["request"]
    entry = args["entry"]
    
    data = req.get_data()
    entry_list = data.get("entry_list", [])
    if len(entry_list) == 1:
        config = req.get_configuration()
        tmpl = config.get("entry_title_template", ":: %(title)s")
        entry["entry_title"] = tmpl % {"title": entry_list[0].get("title", "No title")}

    return args
