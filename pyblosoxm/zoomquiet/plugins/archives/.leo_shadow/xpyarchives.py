#@+leo-ver=4-thin
#@+node:zoomq.20100419111908.3769:@shadow pyarchives.py
#@@language python
#@@tabwidth -4
# -*- coding: utf-8 -*-
#@+others
#@+node:zoomq.20100419111908.3770:pyarchives declarations
# vim: tabstop=4 shiftwidth=4
"""
- zoomq 100419 fixed for export month/year with count
Walks through your blog root figuring out all the available monthly archives in
your blogs.  It generates html with this information and stores it in the
$archivelinks variable which you can use in your head or foot templates.

You can format the output with the key "archive_template".

A config.py example:

    py['archive_template'] = '<li><a href="%(base_url)s/%(Y)s/%(b)s">%(m)s/%(y)s</a></li>'

Displays the archives as list items, with a month number slash year number, like 06/78.

The vars available with typical example values are:
    b      'Jun'
    m      '6'
    Y      '1978'
    y      '78'


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

Copyright 2004, 2005 Wari Wahab
"""
__author__ = "Wari Wahab - wari at wari dot per dot sg"
__version__ = "$Id$"

from Pyblosxom import tools
import time, os

#@-node:zoomq.20100419111908.3770:pyarchives declarations
#@+node:zoomq.20100419111908.3771:verify_installation
def verify_installation(request):
    config = request.get_configuration()
    if not config.has_key("archive_template"):
        print "missing optional config property 'archive_template' which "
        print "allows you to specify how the archive links are created.  "
        print "refer to pyarchive plugin documentation for more details."
    return 1

#@-node:zoomq.20100419111908.3771:verify_installation
#@+node:zoomq.20100419111908.3772:class PyblArchives
class PyblArchives:
    #@    @+others
    #@+node:zoomq.20100419111908.3773:__init__
    def __init__(self, request):
        self._request = request
        self._archives = None

    #@-node:zoomq.20100419111908.3773:__init__
    #@+node:zoomq.20100419111908.3774:__str__
    def __str__(self):
        if self._archives == None:
            self.gen_linear_archive()
        return self._archives

    #@-node:zoomq.20100419111908.3774:__str__
    #@+node:zoomq.20100419111908.3775:gen_linear_archive
    def gen_linear_archive(self):
        config = self._request.get_configuration()
        data = self._request.get_data()
        root = config["datadir"]
        archives = {}
        archive_list = tools.walk(self._request, root)
        fulldict = {}
        fulldict.update(config)
        fulldict.update(data)
        template = config.get('archive_template', 
                    '<a href="%(base_url)s/%(Y)s/%(m)s">%(y)s.%(m)s</a>')
        #<a href="%(base_url)s/%(Y)s/%(b)s">%(Y)s-%(b)s</a>
        #print fulldict["base_url"]
        for mem in archive_list:
            timetuple = tools.filestat(self._request, mem)
            timedict = {}
            for x in ["B", "b", "m", "Y", "y"]:
                timedict[x] = time.strftime("%" + x, timetuple)
            fulldict.update(timedict)
            if not archives.has_key(timedict['Y'] + timedict['m']):
                archives[timedict['Y'] + timedict['m']] = [template % fulldict,1]
            else:
                archives[timedict['Y'] + timedict['m']][1] += 1
                archives[timedict['Y'] + timedict['m']][0] = template % fulldict
        #print archives
        #return
        arc_keys = archives.keys()
        arc_keys.sort()
        arc_keys.reverse()
        #@    @+others
        #@+node:zoomq.20100419194136.6323:gen_year_month_account
        yearmonth = {}
        result = []
        #base archives walk and count every year's mounth
        for key in arc_keys:
            yearname = key[:-2]
            if yearname in yearmonth.keys():
                yearmonth[yearname][0] += archives[key][1]
                yearmonth[yearname][1].append(archives[key])
            else:
                yearmonth[yearname] = [archives[key][1],[]]
                yearmonth[yearname][1].append(archives[key])
        #print yearmonth["2007"]
        mon_keys = yearmonth.keys()
        mon_keys.sort()
        mon_keys.reverse()
        #print mon_keys
        for year in mon_keys:
            #print "%s<sup>%s<sup>"%(year,yearmonth[year][0])
            monode = yearmonth[year][1]
            result.append("<li class='yearchives'><a href='%s'>%s</a><sup>(%d)</sup></li>"%(fulldict["base_url"],year,yearmonth[year][0]))
            if 1==len(monode):
                #print "%s<sup>%s<sup>"%(monode[0][0],monode[0][1])
                result.append("<li>%s<sup>(%d)</sup><li>"%(monode[0][0],monode[0][1]))
            else:
                for m in monode:
                    #print m
                    #print "%s<sup>%s<sup>"%(m[0],m[1])
                    result.append("<li>%s<sup>(%d)</sup><li>"%(m[0],m[1]))
                    #result.append("%s<sup>%s<sup>"%(month[0],month[1]))

        #@-node:zoomq.20100419194136.6323:gen_year_month_account
        #@-others
        #print result
        self._archives = '\n'.join(result)

    #@-node:zoomq.20100419111908.3775:gen_linear_archive
    #@-others
#@-node:zoomq.20100419111908.3772:class PyblArchives
#@+node:zoomq.20100419111908.3776:cb_prepare
def cb_prepare(args):
    request = args["request"]
    data = request.get_data()
    data["archivelinks"] = PyblArchives(request)
#@-node:zoomq.20100419111908.3776:cb_prepare
#@-others
#@-node:zoomq.20100419111908.3769:@shadow pyarchives.py
#@-leo
