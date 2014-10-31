# coding=utf-8
import os


class SemanticHierarchyAnalyzer:
    def __init__(self, semantic_list_path=None):
        if semantic_list_path is None:
            base_dir = os.path.dirname(__file__)
            semantic_list_path = os.path.join(base_dir, "../model/semantic_hierarchy.lst")
        self.tag_to_parent_tags = {}
        with open(semantic_list_path) as semantic_hierarchy_file:
            for line in semantic_hierarchy_file:
                line = line.strip().decode("utf-8")
                splits = line.split(chr(127))
                tag = splits[0]
                parent_tags = splits[1:][::-1]
                self.tag_to_parent_tags[tag] = parent_tags

    def get_hierarchy_tags(self, word):
        return self.tag_to_parent_tags[word]


if __name__ == "__main__":
    semantic_hierarchy = SemanticHierarchyAnalyzer()
    print semantic_hierarchy.get_parent_semantic_tags(u"安道尔")