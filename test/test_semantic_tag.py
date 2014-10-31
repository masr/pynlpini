# coding=utf-8
import unittest
from pynlpini import SemanticTagger
import os


class SemanticTagTestCase(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.analyzer = SemanticTagger(os.path.join(base_dir, "./data/semantic_tag.lst"))

    def tearDown(self):
        pass

    def testSemanticHierarchy(self):
        res = self.analyzer.get_tags(u'张拱贵')
        self.assertEqual(len(res), 1)
        self.assertEquals(set(res[0]), set([u'苏州大学', u'名人', u'中国语言学家', u'知名人物', u'语言学家']))
        res = self.analyzer.get_tags(u'江文虎')
        self.assertEqual(len(res), 2)
        self.assertEquals(set(res[0]), set([u'官员', u'人物']))
        self.assertEquals(set(res[1]), set([u'演员', u'人物']))

if __name__ == "__main__":
    unittest.main()