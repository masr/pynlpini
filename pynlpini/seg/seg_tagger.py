# coding=utf-8

import CRFPP
from pynlpini.seg.tag_seg_txt import normalize
import os
import time


class SegTagger:
    total_model_time = 0

    def __init__(self, model_path=None, args="-v 3 -n1"):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "./../model/seg.crf.model")
        if args is None:
            args = "-v 3 -n1"
        self.model = CRFPP.Tagger("-m " + model_path + " " + args)

    def seg_as_txt(self, txt):
        return ' '.join(self.seg_as_iter(txt))

    def seg_with_label(self, txt):
        if type(txt) != unicode:
            raise "the text must be unicode type"
        lines = txt.split("\n")
        for line_no, line in enumerate(lines):
            new_line = normalize(line)
            t1 = time.time()
            self.model.clear()
            t2 = time.time()
            self.total_model_time += t2 - t1
            for c in new_line:
                if c == " ":
                    c = "|"
                t1 = time.time()
                self.model.add(c.encode("utf-8"))
                t2 = time.time()
                self.total_model_time += t2 - t1
            t1 = time.time()
            self.model.parse()
            t2 = time.time()
            self.total_model_time += t2 - t1
            for idx, c in enumerate(line):
                t1 = time.time()
                yield self.model.y2(idx)
                t2 = time.time()
                self.total_model_time += t2 - t1
            if line_no < len(lines) - 1:
                yield "\n"

    def seg_as_iter(self, txt):
        segs = self.seg_with_label(txt)
        result = ""
        for idx, label in enumerate(segs):
            c = txt[idx]
            if label == "S" or label == "\n":
                yield c
            else:
                result += c
                if label == "E":
                    yield result
                    result = ""


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    tagger = SegTagger(base_dir + "/../model/seg.crf.model")
    result = tagger.seg_as_txt(
        u"本书源自作者在斯坦福大学教授多年的Web挖掘课程材料，主要关注随机流平面和余弦距离和大数据环境下数据挖掘的实际算法。书中分析了海量数据集数据挖掘常用的算法，介绍了目前Web应用的许多重要话题。主要内容包括")
    result = tagger.seg_as_txt(u"千岛湖东南湖区船票+门票")

    print result
