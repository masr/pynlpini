# coding=utf-8

import os

from pynlpini.common import chinese_processor
from pipe import *


class KeywordExtractor:
    def __init__(self, seg_tagger):
        self.seg_tagger = seg_tagger
        base_dir = os.path.dirname(__file__)
        idf_file_path = os.path.join(base_dir, "./../dict/idf.csv")
        idf = dict()
        with open(idf_file_path) as idf_file:
            for line in idf_file:
                line = line.strip().decode("utf-8")
                splits = line.split()
                idf[splits[0]] = float(splits[1])
        self.median_idf = sorted(idf.values())[len(idf) / 2]
        self.idf = idf


    def extract(self, txt, top_k=20):
        if type(txt) != unicode:
            raise "txt must be unicode!"
        words = self.seg_tagger.seg_as_iter(txt)
        freq = {}
        for w in words:
            if len(w) <= 1 or w in chinese_processor.STOP_WORD_SET:
                continue
            freq[w] = freq.get(w, 0.0) + 1.0
        total = sum(freq.values())
        freq = [(k, f) for k, f in freq.iteritems()]

        tf_idf_list = [(f * self.idf.get(k, self.median_idf), k, f) for k, f in freq]
        st_list = sorted(tf_idf_list, reverse=True)

        top_tuples = st_list[:top_k]
        return top_tuples | select(lambda x: [x[1], x[2]]) | as_list


if __name__ == '__main__':
    from pynlpini.seg.seg_tagger import SegTagger

    extractor = KeywordExtractor(SegTagger())
    print extractor.extract(
        u"太乙峰，太乙真人修道成仙的地方，蒋介石1926第一次来庐山居住的村庄！大汉阳锋，庐山最高峰，海拔1474米.五老峰，形似毛主席头像，庐山第二高峰，海拔1368米.含鄱口，庐山第三高峰，海拔1286米，可以远眺中国最大的淡水湖•鄱阳湖！水杉林，庐山植物园的秋天是最美的，秋如醉！好多小猕猴，好可爱，跟游客要东西吃！庐山迎客松，毛主席为江青同志题诗的地方.暮色苍茫看劲松，乱云飞渡人从容.狮子口悬崖险峰，锦绣谷最高点，海拔1025米.天生一个仙人洞，无限风光在险峰.如琴湖，庐山第二大人工湖！形似小提琴，水如琴声！太丢人了，游客拍的发给我的！中国最大的淡水湖•鄱阳湖和中国最长的河流•长江的交汇点，鄱阳湖入长江的口岸，长江的中游与下游的分界线，历代兵家必争的要塞！灯塔，指引夜航者的航标，点燃希望的路标！在这山花烂漫的日子，我的心又开始蠢蠢欲动了！岩缝中的小生命，坚强的生命！山中小山村远看也很美！苏东坡《石钟山记》中的那座小山，历代兵家必争的要塞！景德镇，中华的瓷都，千年的瓷都！郭沫若先生曾写过：“中华向号瓷之国，瓷业高峰是瓷都.”中国最美的廊桥之一，《闪闪的红星》的拍摄地！山环水绕，青山绿水，廊桥遗梦！婺源，美丽的水乡！走江西全线，一定得做好心理和体力准备，因为全是爬山，很累，尤其是爬三清山！跟团游")