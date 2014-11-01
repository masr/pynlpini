# coding=utf-8

import re
from pynlpini import chinese_processor
import itertools
from pipe import *
from pynlpini import PosTagger
from pynlpini import SegTagger


class ImpressionExtractor:
    def __init__(self, pos_tagger):
        self.pos_tagger = pos_tagger


    def extract(self, txt):
        if type(txt) != unicode:
            raise "txt must be unicode!"

        def process_tag(tag):
            if tag[0] in [u"不", u"没", u"没有"] and tag[1] == "ad":
                return (tag[0], "no")
            return tag

        # print txt
        lines = txt.split("\n")
        cur_index = 0
        for line in lines:
            tags = self.pos_tagger.pos_as_iter(line) | select(process_tag) | as_list
            # for tag in tags:
            #     print tag[0] + "(" + tag[1] + ")",
            # print ""
            words = [tag[0] for tag in tags]
            flags_with_index = [tag[1] + "_" + str(idx) for idx, tag in enumerate(tags)]
            # valid_flag_sequence_str = ''.join(
            # range(len(words)) | where(lambda idx: words[idx] not in cp.STOP_WORD_SET) | select(
            # lambda idx: flags_with_index[idx]))
            valid_flag_sequence_str = ''.join(flags_with_index)


            def extract_nums(txt):
                return re.compile("\d+").findall(txt) | select(int)

            pats = [("((nn_\d+)+)(ad_\d+)*((va_\d+)+)", [0, 3]),  # 装修很精致->装修精致, 装修精致->装修精致，材料音质非常干净简单->材料音质干净简单
                    ("((nn_\d+)+)(no_\d+)(va_\d+)", [0, 2, 3]),  # 菜不好吃->菜不好吃
                    ("((ad_\d+)*)((jj_\d+)+)deg_\d+((nn_\d+)+)", [4, 2])]  # 很小的饭店->店小, 非常非常不错的地方->地方不错，美味好吃的鱼->鱼美味好吃

            for pat in pats:
                pattern = pat[0]
                orders = pat[1]
                for matches in re.compile(pattern).findall(valid_flag_sequence_str):
                    short_matches = [matches[idx] for idx in orders] \
                                    | select(extract_nums) \
                                    | select(lambda nums: [words[num] for num in nums]) \
                                    | select(lambda words: ''.join(words)) \
                                    | as_list
                    short_phrase = ''.join(short_matches)
                    first_index = matches | select(extract_nums) | chain | min
                    last_index = matches | select(extract_nums) | chain | max
                    complete_phrase = ''.join(words[first_index:last_index + 1])
                    index = cur_index + ([len(words[i]) for i in range(first_index)] | add)
                    yield (short_phrase, complete_phrase, index)

            cur_index += len(line) + 1


if __name__ == '__main__':
    with  open("../../data/app/travel_comments/mafengwo_comments_raw.txt") as comment_file:
        index = 0
        ie = ImpressionExtractor(PosTagger(SegTagger()))
        for line in comment_file:
            line = line.decode("utf-8")
        for item in ie.extract(line):
            print item
        index += 1
        if index > 10:
            exit()


