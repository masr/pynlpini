# coding=utf-8
import CRFPP
from pynlpini.ner.tag_ner_txt import normalize
import os


class NerTagger:
    def __init__(self, model_path=None, args="-v 3 -n1"):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "./../model/ner.crf.model")
        if args is None:
            args = "-v 3 -n1"
        self.tagger = CRFPP.Tagger("-m " + model_path + " " + args)

    def ner_as_iter(self, txt):
        if type(txt) != unicode:
            raise "the text must be unicode type"
        lines = txt.split("\n")
        cur_index = 0
        for line in lines:
            if len(line) != 0:
                new_line = normalize(line)
                self.tagger.clear()
                for c in new_line:
                    if c == " ":
                        c = "|"
                    self.tagger.add(c.encode("utf-8"))
                self.tagger.parse()
                meet_ner = False
                ner_type = ""
                ner = ""
                for idx, c in enumerate(line):
                    label = self.tagger.y2(idx)
                    if label == 'N':
                        if meet_ner:
                            yield (ner, ner_type, cur_index - len(ner))
                            ner = ""
                        meet_ner = False
                    else:
                        if not meet_ner:
                            meet_ner = True
                        ner_type = label.split("-")[1]
                        ner += c
                    cur_index += 1
            cur_index += 1


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    tagger = NerTagger(base_dir + "/../model/ner.crf.model")
    result = tagger.ner_as_iter(
        u"我叫胡锦涛,我发现周杰人很好,本书源自作者在斯坦福大学教授多年的Web挖掘课程材料，曾经游览过封阳县及周边,我叫胡锦涛.")
    print list(result)
    result = tagger.ner_as_iter(
        u"苏州，古称吴，简称苏，又称姑苏、平江等，中国华东地区特大城市之一，位于江苏省东南部、长江以南、太湖东岸、长江三角洲中部。")
    print list(result)