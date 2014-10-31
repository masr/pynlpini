# coding=utf-8

import os
from _collections import defaultdict


class SemanticTagger:
    def __init__(self, semantic_list_path=None):
        if semantic_list_path is None:
            base_dir = os.path.dirname(__file__)
            semantic_list_path = os.path.join(base_dir, "../model/semantic_tag.lst")
        self.name_to_tags = defaultdict(list)
        with open(semantic_list_path) as semantic_tag_file:
            for line in semantic_tag_file:
                line = line.strip().decode("utf-8")
                splits = line.split(chr(127))
                name = splits[0]
                tags = splits[1:]
                self.name_to_tags[name].append(tags)

    def get_tags(self, word):
        return self.name_to_tags[word]


if __name__ == "__main__":
    semantic_tagger = SemanticTagger()
    print semantic_tagger.get_tags(u"张拱贵")