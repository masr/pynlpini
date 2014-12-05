# coding=utf-8
__author__ = 'maosuhan'

import json
import os

from flask import Flask
from flask import request, abort
from pynlpini import Word2Vector
from jieba.analyse import extract_tags
from pipe import *


app = Flask(__name__)
print __file__
base_dir = os.path.dirname(__file__)

phrase2vector = Word2Vector.get_phrase_model()
vocabs = phrase2vector.vocab.keys()
word2vector = Word2Vector.get_word_model()

with open(base_dir + "/tag.csv") as tag_file:
    tags = [line.decode("utf-8").strip() for line in tag_file.readlines()]


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
    words = extract_tags(text, 100) | where(lambda x: x in vocabs) | as_list
    tags_result = tags | select(lambda tag: [tag, phrase2vector.n_similarity(words, [tag])]) | sort(
        key=lambda x: x[1], reverse=True) | as_list
    return json.dumps(tags_result, ensure_ascii=False)

@app.route('/tag2', methods=['GET', 'POST'])
def tag():
    global word2vector
    if request.args.get('txt') is None:
        if request.form.get('txt') is None:
            abort(400)
        else:
            text = request.form.get('txt')
    else:
        text = request.args.get('txt')
    words = extract_tags(text, 100) | where(lambda x: x in vocabs) | as_list
    tags_result = tags | select(lambda tag: [tag, word2vector.n_similarity(words, [tag])]) | sort(
        key=lambda x: x[1], reverse=True) | as_list
    return json.dumps(tags_result, ensure_ascii=False)


def run(**kwargs):
    app.run(**kwargs)


if __name__ == '__main__':
    app.debug = True
    app.run(port=7000, host="0.0.0.0")