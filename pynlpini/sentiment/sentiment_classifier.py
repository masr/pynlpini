# coding=utf-8


import os
from pynlpini.lib.libsvm import svmutil
from pynlpini.lib.libsvm import svm
from pynlpini.seg.seg_tagger import SegTagger
from pipe import *
import json
from pynlpini.sentiment.tag_sentiment_txt import get_features


class SentimentClassifier:
    def __init__(self, seg_tagger, sentiment_model_path=None, feature_index_path=None):
        if sentiment_model_path is None:
            sentiment_model_path = os.path.join(os.path.dirname(__file__), "./../model/sentiment.svm.model")
        if feature_index_path is None:
            feature_index_path = os.path.join(os.path.dirname(__file__), "./../model/sentiment_feature_index.json")
        self.model = svmutil.svm_load_model(sentiment_model_path)
        with open(
                feature_index_path) as feature_index_dict_file:
            self.feature_index_dict = json.load(feature_index_dict_file, encoding="utf-8")
        self.tagger = seg_tagger

    def classifier(self, txt):
        seged_txt = self.tagger.seg_as_txt(txt)
        features = get_features(seged_txt)
        feature_indexes = []
        for feature in features:
            if feature in self.feature_index_dict:
                feature_indexes.append(self.feature_index_dict[feature])
            else:
                continue
        feature_index_set = sorted(set(feature_indexes))
        feature_index_with_weight = feature_index_set | select(
            lambda index: (index, feature_indexes.count(index))) | as_dict
        x, max_idx = svm.gen_svm_nodearray(feature_index_with_weight)
        label = svm.libsvm.svm_predict(self.model, x)
        return label


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    classfifier = SentimentClassifier(SegTagger(), os.path.join(base_dir, "./../model/sentiment.svm.model"),
                                      os.path.join(base_dir, "./../model/sentiment_feature_index.json"))

    def classifier(txt):
        print txt + " " + str(classfifier.classifier(txt))

    classifier(u"这个东西非常糟糕！")
    classifier(u"太坑爹了")
    classifier(u"感觉不是很满意")
    classifier(u"很不错啊！")
    classifier(u"太坑爹了")
    classifier(u"很多毛病")
    classifier(u"就是我想要的！封面很漂亮！")
    classifier(u"床板很硬，菜也不卫生")
    classifier(u"服务员不咋地")
    classifier(u"主人很热情，我们一家住的很舒心")
    classifier(u"丝毫没有必要来")
    classifier(u"风景很美")
    classifier(u"赞！不能同意更多")



