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
            u"参观的人不多，这家私房菜的菜式口味偏重，秘制酱汁是他家的特色，非常合我的胃口！\n做法很独特，味道也正！\n和大多数私房菜一样，食锦记也有属于自己的精致餐具。。。。从外面看还是不错的，特有感觉的一家店，这里是个装修非常精致典雅的小茶馆，感觉是个很好的饭店。")
        res = set(res)
        # for i in res:
        #     print i[0], i[1], i[2]
        self.assertEquals(res,
                          set([(u'人不多', u'人不多', 3), (u'口味偏重', u'口味偏重', 15), (u'做法独特', u'做法很独特', 40),
                               (u'装修精致典雅', u'装修非常精致典雅', 103),
                               (u'饭店好', u'很好的饭店', 120), (u'私房菜一样', u'私房菜一样', 56)]))


if __name__ == "__main__":
    unittest.main()