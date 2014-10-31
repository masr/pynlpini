# coding=utf-8

import re
import pynlpini.common.chinese_processor as cp
import itertools
from pipe import *
from pynlpini.pos.pos_tagger import PosTagger
from pynlpini.seg.seg_tagger import SegTagger


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
            # print tag[0] + "(" + tag[1] + ")",
            # print ""
            words = [tag[0] for tag in tags]
            flags_with_index = [tag[1] + "_" + str(idx) for idx, tag in enumerate(tags)]
            valid_flag_sequence_str = ''.join(
                range(len(words)) | where(lambda idx: words[idx] not in cp.STOP_WORD_SET) | select(
                    lambda idx: flags_with_index[idx]))


            def extract_from_patterns(patterns):
                pattern = re.compile("(" + ")|(".join(patterns) + ")")
                for m in pattern.finditer(valid_flag_sequence_str):
                    group = m.group(0)
                    digit_pattern = re.compile("\d+")
                    indexes = digit_pattern.findall(group)
                    short_phrase = ''.join(indexes | select(lambda idx: words[int(idx)]))
                    complete_phrase = ''.join(words[int(indexes[0]):int(indexes[-1]) + 1])
                    yield (short_phrase, complete_phrase,
                           cur_index + (range(int(indexes[0])) | select(lambda x: len(tags[x][0])) | add) )

            for item in itertools.chain(extract_from_patterns(
                    ["(nn_\d+)+(ad_\d+)*(va_\d+)+",  # 装修很精致
                     "(nn_\d+)+(no_\d+)(va_\d+)",  # 菜不好吃
                     "(ad_\d+)+(jj_\d+)+(nn_\d+)+"])):  # 很小的饭店
                yield item

            cur_index += len(line) + 1


if __name__ == '__main__':
    with open("../../data/app/travel_comments/mafengwo_comments_raw.txt") as comment_file:
        index = 0
        ie = ImpressionExtractor(PosTagger(SegTagger()))
        for line in comment_file:
            line = line.decode("utf-8")
        for item in ie.extract(line):
            print item
        index += 1
        if index > 10:
            exit()


