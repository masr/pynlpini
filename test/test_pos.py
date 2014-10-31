# coding=utf-8
import unittest
import os

from pynlpini import PosTagger
from pynlpini import SegTagger


class PosTaggerTestCase(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.pos_tagger = PosTagger(SegTagger(), os.path.join(base_dir, "./model/pos.crf.model"))

    def tearDown(self):
        pass

    def testPosTagger(self):
        res = self.pos_tagger.pos_as_iter(u"据以色列电台昨天报道")
        self.assertEquals(list(res), [(u"据", "p"), (u"以色列", "nr"), (u"电台", "nn"), (u"昨天", "nt"), (u"报道", "vv")])

    def testPosTaggerWithMultipleLines(self):
        res = self.pos_tagger.pos_as_iter(u"据以色列电台昨天报道\n\n 巴勒斯坦和以色列")
        self.assertEquals(list(res),
                          [(u"据", "p"), (u"以色列", "nr"), (u"电台", "nn"), (u"昨天", "nt"), (u"报道", "vv"), ("\n", "pu"),
                           ("\n", "pu"), (" ", "pu"), (u"巴勒斯坦", "nr"), (u"和", "cc"), (u"以色列", "nr")])


if __name__ == "__main__":
    unittest.main()