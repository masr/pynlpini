# coding=utf-8
import unittest
from pynlpini import NerTagger
import os


class NerTaggerTestCase(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.ner_tagger = NerTagger(os.path.join(base_dir, "./model/ner.crf.model"))

    def tearDown(self):
        pass

    def testNerTagger(self):
        res = self.ner_tagger.ner_as_iter(u"尤以收录周恩来总理\n\n吊脚楼茶馆，坐落在栋梁河边的悬崖上")
        self.assertEquals(list(res), [(u"周恩来", "PER", 4), (u"栋梁河", "LOC", 20)])


if __name__ == "__main__":
    unittest.main()