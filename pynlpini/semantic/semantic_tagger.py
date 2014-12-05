# # coding=utf-8
# import json
#
#
# class SemanticTagger:
#     def __init__(self):
#         self.redis = redis.Redis(host='localhost', port=6499)
#
#     def get_tags(self, word):
#         return json.loads(self.redis.hget("pynlpini", word))
#
#
# if __name__ == "__main__":
#     semantic_tagger = SemanticTagger()
#     print semantic_tagger.get_tags(u"张拱贵")