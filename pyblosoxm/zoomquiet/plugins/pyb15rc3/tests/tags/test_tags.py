import tempfile
import shutil
import os

from plugins.tests.test_base import PluginTest
from plugins.tags import tags
from Pyblosxom.pyblosxom import Request

class TagsTest(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, tags)
        self.tmpdir = tempfile.mkdtemp() 

    def get_datadir(self):
        return os.path.join(self.tmpdir, "datadir")

    def tearDown(self):
        PluginTest.tearDown(self)
        try:
            shutil.rmtree(self.tmpdir)
        except OSError:
            pass
                
    def test_get_tagsfile(self):
        req = Request({"datadir": self.get_datadir()}, {}, {})

        cfg = {"datadir": self.get_datadir()}
        self.assertEquals(tags.get_tagsfile(cfg),
                          os.path.join(self.get_datadir(), os.pardir,
                                       "tags.index"))
        
        tags_filename = os.path.join(self.get_datadir(), "tags.db")
        cfg = {"datadir": self.get_datadir(), "tags_filename": tags_filename}
        self.assertEquals(tags.get_tagsfile(cfg), tags_filename)

    def test_tag_cloud_no_tags(self):
        # test no tags
        self.request.get_data()["tagsdata"] = {}
        
        tags.cb_head(self.args)
        self.assertEquals(
            str(self.args["entry"]["tagcloud"]),
            "\n".join(
                ["<p>",
                 "</p>"]))

    def test_tag_cloud_one_tag(self):
        # test no tags
        self.request.get_data()["tagsdata"] = {
            "tag2": ["a"],
            }
        
        tags.cb_head(self.args)
        self.assertEquals(
            str(self.args["entry"]["tagcloud"]),
            "\n".join(
                ["<p>",
                 '<a class="bigTag" href="http://bl.og//tag/tag2">tag2</a>',
                 "</p>"]))

    def test_tag_cloud_many_tags(self):
        # test no tags
        self.request.get_data()["tagsdata"] = {
            "tag1": ["a", "b", "c", "d", "e", "f"],
            "tag2": ["a", "b", "c", "d"],
            "tag3": ["a"]
            }
        
        tags.cb_head(self.args)
        self.assertEquals(
            str(self.args["entry"]["tagcloud"]),
            "\n".join(
                ["<p>",
                 '<a class="bigTag" href="http://bl.og//tag/tag1">tag1</a>',
                 '<a class="mediumTag" href="http://bl.og//tag/tag2">tag2</a>',
                 '<a class="smallTag" href="http://bl.og//tag/tag3">tag3</a>',
                 "</p>"]))
