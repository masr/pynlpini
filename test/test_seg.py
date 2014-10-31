# coding=utf-8
import unittest
import os
from pynlpini import SegTagger


class SegTaggerTestCase(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.tagger = SegTagger(os.path.join(base_dir, "./model/seg.crf.model"))

    def tearDown(self):
        pass

    def testSegTagger(self):
        res = self.tagger.seg_as_iter(u"巴勒斯坦和以色列")
        self.assertEquals(list(res), [u"巴勒斯坦", u"和", u"以色列"])
        res = self.tagger.seg_as_txt(u"巴勒斯坦和以色列")
        self.assertEquals(res, u"巴勒斯坦 和 以色列")

    def testSegTaggerWithMultipleLines(self):
        res = self.tagger.seg_as_iter(u"巴勒斯坦和以色列\n\n 吴邦国副总理５号傍晚")
        self.assertEquals(list(res), [u"巴勒斯坦", u"和", u"以色列", "\n", "\n", " ", u"吴邦国", u"副总理", u"５号", u"傍晚"])


if __name__ == "__main__":
    unittest.main()