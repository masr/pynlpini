# coding=utf-8
import unittest
from pynlpini import SemanticHierarchyAnalyzer
import os


class SemanticHierarchyTestCase(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.analyzer = SemanticHierarchyAnalyzer(os.path.join(base_dir, "./data/semantic_hierarchy.lst"))

    def tearDown(self):
        pass

    def testSemanticHierarchy(self):
        res = self.analyzer.get_hierarchy_tags(u'电力')
        self.assertEquals(list(res), [u"电能", u"能源", u"技术"])


if __name__ == "__main__":
    unittest.main()