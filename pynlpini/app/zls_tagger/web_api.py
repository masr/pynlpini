# coding=utf-8
__author__ = 'maosuhan'

import json
import os

from flask import Flask, request, abort
from pynlpini.word2vec.word2vector import Word2Vector
from pynlpini.keyword.keyword_extractor import KeywordExtractor
from pynlpini.seg.seg_tagger import SegTagger
from pipe import *
from collections import defaultdict


app = Flask(__name__)
base_dir = os.path.dirname(__file__)

phrase2vector = Word2Vector.get_phrase_model()
phrase_vocabs = phrase2vector.vocab.keys()
keyword_extractor = KeywordExtractor(SegTagger())
tag_dict = defaultdict(set)

with open(base_dir + "/tag.csv") as tag_file:
    tmp_dict = tag_file.readlines() | select(lambda x: x.decode("utf-8").strip()) | where(
        lambda x: len(x) > 0) | select(
        lambda x: (x.split()[0].strip(), x.split()[1].strip())) | as_dict
    for k, v in tmp_dict.iteritems():
        if k in phrase_vocabs and v in phrase_vocabs:
            tag_dict[v].add(k)


@app.route('/tag', methods=['GET', 'POST'])
def tag():
    global phrase2vector
    if request.args.get('txt') is None:
        if request.form.get('txt') is None:
            abort(400)
        else:
            text = request.form.get('txt')
    else:
        text = request.args.get('txt')
    words = keyword_extractor.extract(text, 50) | where(lambda x: x[0] in phrase_vocabs) | select(
        lambda x: [x[0] for i in range(x[1])]) | chain | as_list
    tags_result = tag_dict.keys() | select(lambda tag: [tag, phrase2vector.n_similarity(words, tag_dict[tag])]) | sort(
        key=lambda x: x[1], reverse=True) | as_list
    return json.dumps(tags_result, ensure_ascii=False)


def run(**kwargs):
    app.run(**kwargs)


if __name__ == '__main__':
    app.debug = True
    app.run(port=7000, host="0.0.0.0")