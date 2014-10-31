# coding=utf-8
import unittest
from pynlpini import ImpressionExtractor
from pynlpini import PosTagger
from pynlpini import SegTagger


class ImpressionExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = ImpressionExtractor(
            PosTagger(SegTagger()))

    def tearDown(self):
        pass

    def testImpressionExtractor(self):
        res = self.extractor.extract(
            u"参观的人不多，这家私房菜的菜式口味偏重，秘制酱汁是他家的特色，非常合我的胃口！\n做法很独特，味道也正！\n和大多数私房菜一样，食锦记也有属于自己的精致餐具。。。。从外面看你还是不错的，特有感觉的一家店，这里是个装修精致的小茶馆，感觉是个很好的饭店。")
        self.assertEquals(list(res),
                          [(u'人不多', u'人不多', 3), (u'口味偏重', u'口味偏重', 15), (u'做法很独特', u'做法很独特', 40),
                           (u'装修精致', u'装修精致', 104),
                           (u'很好饭店', u'很好的饭店', 117)])


if __name__ == "__main__":
    unittest.main()