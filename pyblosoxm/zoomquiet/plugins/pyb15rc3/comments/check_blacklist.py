#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
# 2011 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

This works in conjunction with the comments plugin and allows you to
xreduce comment spam by a words blacklist.  Any comment that contains
one of the blacklisted words will be rejected immediately.

This shouldn't be the only way you reduce comment spam.  It's probably
not useful to everyone, but would be useful to some people as a quick
way of catching some of the comment spam they're getting.


Usage
=====

For setup, all you need to do is set the comment_rejected_words
property in your config.py file.  For example, the following will
reject any incoming comments with the words ``gambling`` or ``casino``
in them::

   py["comment_rejected_words"] = ["gambling", "casino"]


The comment_rejected_words property takes a list of strings as a
value.

.. Note::

   There's a deficiency in the algorithm.  Currently, it will match
   substrings, too.  So if you blacklist the word "word", that'll nix
   comments with "word" in it as well as comments with "crossword"
   because "word" is a substring of "crossword".

   Pick your blacklisted words carefully or fix the algorithm!

.. Note::

   This checks all parts of the comment including the ip address of
   the poster.  Blacklisting ip addresses is as easy as adding the ip
   address to the list::

      py["comment_rejected_words"] = ["192.168.1.1", ...]

Additionally, the wbgcomments_blacklist plugin can log when it
blacklisted a comment and what word was used to blacklist it.
Sometimes this information is interesting.  True, "yes, I want to log"
and False (default) if "no, i don't want to log".  Example::

   py["comment_rejected_words_log"] = False
"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2011-01-25"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "Rejects comments that contain specified blacklisted words."
__category__ = "comments"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


import time
import os.path

def verify_installation(request):
    config = request.get_configuration()
    if not "comment_rejected_words" in config:
        print "The \"comment_rejected_words\" property must be set in your config.py "
        print "file.  It takes a list of strings as a value.  Refer to the "
        print "documentation at the top of the comment_blacklist plugin for more "
        print "details."
        return 0

    crw = config["comment_rejected_words"]
    if not (isinstance(crw, list) or isinstance(crw, tuple)):
        print "The \"comment_rejected_words\" property is incorrectly set in your "
        print "config.py file.  It takes a list of strings as a value.  Refer to "
        print "the documentation at the top of the comment_blacklist plugin for "
        print "more details."
        return 0
    return 1


def cb_comment_reject(args):
    r = args["request"]
    c = args["comment"]

    config = r.get_configuration()

    badwords = config.get("comment_rejected_words", [])
    for mem in c.values():
        mem = mem.lower()
        for word in badwords:
            # FIXME - this matches on substrings, too.  should use
            # word-boundaries.
            if mem.find(word) != -1:
                if ((config.get("comment_rejected_words_log", False) and
                     "logdir" in config)):
                    fn = os.path.join(config["logdir"], "blacklist.log")
                    f = open(fn, "a")
                    f.write("%s: %s %s\n" % (
                            time.ctime(), c.get("ipaddress", None), word))
                    f.close()
                return (True, "Comment rejected: contains blacklisted words.")

    return False
