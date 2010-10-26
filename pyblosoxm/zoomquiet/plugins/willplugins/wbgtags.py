"""
Summary
=======

This is a tags plugin.  It uses PyBlosxom 1.5's command line abilities
to split generation of tags index data from display of tags index
data.

It creates a ``$(tagslist)`` variable for head and foot templates
which lists all the tags.

It creates a ``$(tags)`` variable for story templates which lists tags
for the story.


Configuration
=============

The following config properties define where the tags file is located,
how tag metadata is formatted, and how tag lists triggered.

``tags_separator``

    This defines the separator between tags in the metadata line.
    Defaults to ",".

    After splitting on the separator, each individual tag is stripped
    of whitespace before and after the text.

    For example::

       Weather in Boston
       #tags weather, boston
       <p>
         The weather in Boston today is pretty nice.
       </p>

    returns tags ``weather`` and ``boston``.

    If the ``tags_separator`` is::

       py["tags_separator"] = "::"

    then tags could be declared in the entries like this::

       Weather in Boston
       #tags weather::boston
       <p>
         The weather in Boston today is pretty nice.
       </p>

``tags_filename``

    This is the file that holds indexed tags data.  Defaults to
    datadir + os.pardir + ``tags.index``.

    This file needs to be readable by the process that runs your blog.
    This file needs to be writable by the process that creates the
    index.

``tags_trigger``

    This is the url trigger to indicate that the tags plugin should
    handle the file list based on the tag.  Defaults to ``tag``.


In the head and foot templates, you can list all the tags with the
``$(tagslist)`` variable.  The templates for this listing use the
following three config properties:

``tags_list_start``

    Printed before the list.  Defaults to ``<p>``.

``tags_list_item``

    Used for each tag in the list.  There are a bunch of variables you can
    use:

    * ``base_url`` - the baseurl for your blog
    * ``flavour`` - the default flavour or flavour currently showing
    * ``tag`` - the tag name
    * ``count`` - the number of items that are tagged with this tag
    * ``tagurl`` - url composed of baseurl, trigger, and tag

    Defaults to ``<a href="%(tagurl)s">%(tag)s</a> ``.

``tags_list_finish``

    Printed after the list.  Defaults to ``</p>``.


You can list the tags for a given entry in the story template with the
``$(tags)`` variable.  The tag items in the story are formatted with one
configuration property:

``tags_item``

    This is the template for a single tag for an entry.  It can use the
    following bits:

    * ``base_url`` - the baseurl for this blog
    * ``flavour`` - the default flavour or flavour currently being viewed
    * ``tag`` - the tag
    * ``tagurl`` - url composed of baseurl, trigger and tag

    Defaults to ``<a href="%(tagurl)s">%(tag)s</a>``.

    Tags are joined together with ``, ``.


Creating the tags index file
============================

Run::

    pyblosxom-cmd buildtags

from the directory your ``config.py`` is in or::

    pyblosxom-cmd --config=/path/to/config/file buildtags

from anywhere.

This builds the tags index file that the tags plugin requires to
generate tags-based bits for the request.

You should execute this every time you write or update an entry.
Alternatively, you could execute it in a cron job once a day.

.. Note::

   If you're using static rendering, you need to build the tags
   index before you statically render your blog.


Converting from categories to tags
==================================

This plugin has a command that goes through your entries and adds tag
metadata based on the category.  There are some caveats:

1. it assumes entries are in the blosxom format of title, then
   metadata, then the body.

2. it only operates on entries in the datadir.

It maintains the atime and mtime of the file.  My suggestion is to
back up your files (use tar or something that maintains file stats),
then try it out and see how well it works, and figure out if that
works or not.

To run the command do::

    pyblosxom-cmd categorytotags

from the directory your ``config.py`` is in or::

    pyblosxom-cmd --config=/path/to/config/file categorytotags

from anywhere.


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

Copyright 2009 Will Guaraldi Kahn-Greene

Revisions:
1.0 - 2009-06-02 - initial writing
"""

__author__ = "Will Kahn-Greene - willg at bluesock dot org"
__version__ = "1.0"
__url__ = "http://www.bluesock.org/~willg/pyblosxom/"
__description__ = "Tags plugin"

import os
import cPickle as pickle
import shutil

def savefile(filename, tagdata):
    fp = open(filename + ".new", "w")
    pickle.dump(tagdata, fp)
    fp.close()

    # FIXME - this only works on non-Windows operating systems
    shutil.move(filename + ".new", filename)

def loadfile(filename):
    fp = open(filename, "r")
    tagdata = pickle.load(fp)
    fp.close()
    return tagdata

def get_tagsfile(cfg):
    datadir = cfg["datadir"]
    tagsfile = cfg.get("tags_filename",
                       os.path.join(datadir, os.pardir, "tags.index"))
    return tagsfile

def buildtags(command, argv):
    """Builds the tags index.
    """
    import config

    datadir = config.py.get("datadir")
    if not datadir:
        raise ValueError("config.py has no datadir property.")

    sep = config.py.get("tags_separator", ",")
    tagsfile = get_tagsfile(config.py)

    from Pyblosxom import pyblosxom
    from Pyblosxom import tools
    from Pyblosxom.entries import fileentry

    data = {}

    # register entryparsers so that we parse all possible file types.
    data["extensions"] = tools.run_callback("entryparser",
                                            {"txt": pyblosxom.blosxom_entry_parser},
                                            mappingfunc=lambda x, y:y,
                                            defaultfunc=lambda x: x)

    req = pyblosxom.Request(config.py, {}, data)

    # grab all the entries in the datadir
    filelist = tools.walk(req, datadir)
    entrylist = [fileentry.FileEntry(req, e, datadir) for e in filelist]

    tags_to_files = {}
    for mem in entrylist:
        tagsline = mem["tags"]
        if not tagsline:
            continue
        tagsline = [t.strip() for t in tagsline.split(sep)]
        for t in tagsline:
            tags_to_files.setdefault(t, []).append(mem["filename"])

    savefile(tagsfile, tags_to_files)
    return 0

def category_to_tags(command, argv):
    """Goes through all entries and converts the category to tags
    metadata.

    It adds the tags line as the second line.

    It maintains the mtime for the file.
    """
    import config

    datadir = config.py.get("datadir")
    if not datadir:
        raise ValueError("config.py has no datadir property.")

    sep = config.py.get("tags_separator", ",")
    tagsfile = get_tagsfile(config.py)

    from Pyblosxom import pyblosxom
    from Pyblosxom import tools
    from Pyblosxom.entries import fileentry

    data = {}

    # register entryparsers so that we parse all possible file types.
    data["extensions"] = tools.run_callback("entryparser",
                                            {"txt": pyblosxom.blosxom_entry_parser},
                                            mappingfunc=lambda x, y:y,
                                            defaultfunc=lambda x: x)


    req = pyblosxom.Request(config.py, {}, data)

    # grab all the entries in the datadir
    filelist = tools.walk(req, datadir)

    if not datadir.endswith(os.sep):
        datadir = datadir + os.sep

    for mem in filelist:
        print "working on %s..." % mem

        category = os.path.dirname(mem)[len(datadir):]
        tags = category.split(os.sep)
        print "   adding tags %s" % tags
        tags = "#tags %s\n" % (sep.join(tags))

        atime, mtime = os.stat(mem)[7:9]

        fp = open(mem, "r")
        data = fp.readlines()
        fp.close()

        data.insert(1, tags)

        fp = open(mem, "w")
        fp.write("".join(data))
        fp.close()

        os.utime(mem, (atime, mtime))

    return 0

def cb_commandline(args):
    args["buildtags"] = (buildtags, "builds the tags index")
    args["categorytotags"] = (category_to_tags, "builds tag metadata from categories for entries")
    return args

def cb_start(args):
    request = args["request"]
    data = request.get_data()
    tagsfile = get_tagsfile(request.get_configuration())
    tagsdata = loadfile(tagsfile)
    data["tagsdata"] = tagsdata

def cb_filelist(args):
    # handles /trigger/tag to show all the entries tagged that
    # way
    req = args["request"]

    pyhttp = req.get_http()
    data = req.get_data()
    config = req.get_configuration()

    trigger = "/" + config.get("tags_trigger", "tag")
    if not pyhttp["PATH_INFO"].startswith(trigger):
        return

    datadir = config["datadir"]
    tagsfile = get_tagsfile(config)
    tagsdata = loadfile(tagsfile)

    tag = pyhttp["PATH_INFO"][len(trigger) + 1:]
    filelist = tagsdata.get(tag, [])
    if not filelist:
        tag, ext = os.path.splitext(tag)
        filelist = tagsdata.get(tag, [])
        if filelist:
            data["flavour"] = ext[1:]

    from Pyblosxom.entries import fileentry
    entrylist = [fileentry.FileEntry(req, e, datadir) for e in filelist]

    # sort the list by mtime
    entrylist = [(e._mtime, e) for e in entrylist]
    entrylist.sort()
    entrylist.reverse()
    entrylist = [e[1] for e in entrylist]

    return entrylist

def cb_story(args):
    # adds tags to the entry properties
    request = args["request"]
    entry = args["entry"]
    config = request.get_configuration()

    sep = config.get("tags_separator", ",")
    tags = [t.strip() for t in entry.get("tags", "").split(sep)]
    tags.sort()
    entry["tags_raw"] = tags

    form = request.get_form()
    flavour = (form.has_key('flav') and form['flav'].value or 
               config.get('default_flavour', 'html'))
    baseurl = config.get("base_url", "")
    trigger = config.get("tags_trigger", "tag")
    template = config.get("tags_item", '<a href="%(tagurl)s">%(tag)s</a>')

    tags = [template % {"base_url": baseurl,
                        "flavour": flavour,
                        "tag": tag,
                        "tagurl": "/".join([baseurl, trigger, tag])}
            for tag in tags]
    entry["tags"] = ", ".join(tags)
    return args

def cb_head(args):
    # adds a taglist to header/footer
    request = args["request"]
    entry = args["entry"]
    data = request.get_data()
    config = request.get_configuration()
    tagsdata = data.get("tagsdata", {})

    tags = tagsdata.keys()
    tags.sort()

    start_t = config.get("tags_list_start", '<p>')
    item_t = config.get("tags_list_item", ' <a href="%(tagurl)s">%(tag)s</a> ')
    finish_t = config.get("tags_list_finish", '</p>')

    output = []

    form = request.get_form()
    flavour = (form.has_key('flav') and form['flav'].value or 
               config.get('default_flavour', 'html'))
    baseurl = config.get("base_url", "")
    trigger = config.get("tags_trigger", "tag")

    output.append(start_t)
    for item in tags:
        d = {"base_url": baseurl,
             "flavour": flavour,
             "tag": item,
             "count": len(tagsdata[item]),
             "tagurl": "/".join([baseurl, trigger, item])}
        output.append(item_t % d)
    output.append(finish_t)

    entry["tagslist"] = "\n".join(output)
    return args

cb_foot = cb_head
