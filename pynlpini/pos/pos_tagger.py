# coding=utf-8
import CRFPP
from pynlpini.pos.tag_pos_txt import normalize
import os
from pipe import *


class PosTagger:
    def __init__(self, seg_tagger, model_path=None, args="-v 3 -n1"):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "./../model/pos.crf.model")
        if args is None:
            args = "-v 3 -n1"
        self.pos_model = CRFPP.Tagger("-m " + model_path + " " + args)
        self.seg_tagger = seg_tagger

    def pos_as_iter(self, txt):
        if type(txt) != unicode:
            raise "the text must be unicode type"
        lines = txt.split("\n")
        for line_no, line in enumerate(lines):
            if len(line) == 0:
                yield ("\n", "pu")
            else:
                new_line = normalize(line)
                self.pos_model.clear()
                seg_labels = self.seg_tagger.seg_with_label(new_line) | as_list
                for idx, c in enumerate(new_line):
                    if c == " ":
                        c = "|"
                    self.pos_model.add(c.encode("utf-8") + " " + seg_labels[idx])
                self.pos_model.parse()
                result = ""
                for idx, c in enumerate(line):
                    pos_label = self.pos_model.y2(idx)
                    result += c
                    if seg_labels[idx] in ["S", "E"]:
                        yield (result, pos_label)
                        result = ""
                if line_no < len(lines) - 1:
                    yield ("\n", "pu")


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    tagger = PosTagger(base_dir + "/../model/pos.crf.model")
    result = tagger.pos_as_iter(
        u"本书源自作者在斯坦福大学教授多年的Web挖掘课程材料，主要关注随机流平面和余弦距离和大数据环境下数据挖掘的实际算法。书中分析了海量数据集数据挖掘常用的算法，介绍了目前Web应用的许多重要话题。主要内容包括")
    print result
