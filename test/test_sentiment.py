# coding=utf-8
import unittest
import os

from pynlpini import SegTagger
from pynlpini import SentimentClassifier


class SentimentClassifierTestCase(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.classifier = SentimentClassifier(SegTagger(), os.path.join(base_dir, "./model/sentiment.svm.model"),
                                              os.path.join(base_dir, "./model/sentiment_feature_index.json"))

    def tearDown(self):
        pass

    def testSentimentClassifier(self):
        res = self.classifier.classifier(u"标准间太差 房间还不如3星的 而且设施非常陈旧.建议酒店把老的标准间从新改善.")
        self.assertEqual(res, 0)
        res = self.classifier.classifier(u"距离川沙公路较近,但是公交指示不对,如果是\"蔡陆线\"的话,会非常麻烦.建议用别的路线.房间较为简单.")
        self.assertEqual(res, 1)
        res = self.classifier.classifier(u"预订标准间：拐角房间（为什么携程订的都是拐角间），房间很小，隔音超差，房间非常冷，空调几乎不好用，卫生间更冷，几乎没法淋浴！三个字＂不满意＂！")
        self.assertEqual(res, 0)
        res = self.classifier.classifier(u"商务大床房，房间很大，床有2M宽，整体感觉经济实惠不错!")
        self.assertEqual(res, 1)


if __name__ == "__main__":
    unittest.main()