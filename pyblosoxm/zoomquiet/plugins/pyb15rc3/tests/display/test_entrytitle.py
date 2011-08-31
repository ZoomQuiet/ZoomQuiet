import time
import os

from Pyblosxom import pyblosxom
from plugins.tests.test_base import PluginTest, TIMESTAMP
from plugins.display import entrytitle

class Test_entrytitle(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, entrytitle)

    def test_cb_head(self):
        # no entries yields no entry_title
        args = {
            "request": pyblosxom.Request({}, {}, {}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEquals(newargs["entry"].get("entry_title", ""), "")

        # one entry yields entry_title
        args = {
            "request": pyblosxom.Request(
                {},
                {},
                {"entry_list": [{"title": "foobar"}]}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEquals(newargs["entry"]["entry_title"], ":: foobar")

        # one entry with no title yields entry_title with "No title"
        args = {
            "request": pyblosxom.Request(
                {},
                {},
                {"entry_list": [{}]}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEquals(newargs["entry"]["entry_title"], ":: No title")

        # one entry yields entry_title, using entry_title_template
        # configuration property
        args = {
            "request": pyblosxom.Request(
                {"entry_title_template": "%(title)s ::"},
                {},
                {"entry_list": [{"title": "foobar"}]}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEquals(newargs["entry"]["entry_title"], "foobar ::")

        # multiple entries yields no title
        args = {
            "request": pyblosxom.Request(
                {},
                {},
                {"entry_list": [{"title": "foobar"}, {"title": "foobar2"}]}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEquals(newargs["entry"].get("entry_title", ""), "")

    def test_verify_installation(self):
        self.assert_(entrytitle.verify_installation(self.request))
