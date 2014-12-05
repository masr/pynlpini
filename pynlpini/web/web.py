# coding=utf-8

import json
import os

from pipe import *
from flask import Flask

from pynlpini import SegTagger
from pynlpini import PosTagger
from pynlpini import NerTagger
from pynlpini import ImpressionExtractor
from pynlpini import SentimentClassifier
from pynlpini import Word2Vector


app = Flask(__name__)

base_dir = os.path.dirname(__file__)

seg_tagger = None
pos_tagger = None
ner_tagger = None
impression_extractor = None
sentiment_classifier = None
# semantic_tagger = None
# semantic_hierarchy_analyzer = None
word2vector = None
phrase2vector = None


@app.route('/seg/<txt>')
def seg(txt):
    global seg_tagger
    if seg_tagger is None:
        seg_tagger = SegTagger()
    return json.dumps(seg_tagger.seg_as_iter(txt) | as_list, ensure_ascii=False)


@app.route('/pos/<txt>')
def pos(txt):
    global pos_tagger, seg_tagger
    if seg_tagger is None:
        seg_tagger = SegTagger()
    if pos_tagger is None:
        pos_tagger = PosTagger(seg_tagger)
    return json.dumps(pos_tagger.pos_as_iter(txt) | as_list, ensure_ascii=False)


@app.route('/ner/<txt>')
def ner(txt):
    global ner_tagger
    if ner_tagger is None:
        ner_tagger = NerTagger()
    return json.dumps(ner_tagger.ner_as_iter(txt) | as_list, ensure_ascii=False)


@app.route('/impression/<txt>')
def impression(txt):
    global impression_extractor
    if impression_extractor is None:
        impression_extractor = ImpressionExtractor(pos_tagger)
    return json.dumps(impression_extractor.extract(txt) | as_list, ensure_ascii=False)


@app.route('/sentiment/<txt>')
def sentiment(txt):
    global sentiment_classifier
    if sentiment_classifier is None:
        sentiment_classifier = SentimentClassifier(seg_tagger)
    return str(int(sentiment_classifier.classifier(txt)))


# @app.route('/semantic-tag/<word>')
# def semantic_tag(word):
# from pynlpini import SemanticTagger
#
#     global semantic_tagger
#     if semantic_tagger is None:
#         semantic_tagger = SemanticTagger()
#     return json.dumps(semantic_tagger.get_tags(word), ensure_ascii=False)
#
#
# @app.route('/semantic-hierarchy/<word>')
# def semantic_hierarchy(word):
#     from pynlpini import SemanticHierarchyAnalyzer
#
#     global semantic_hierarchy_analyzer
#     if semantic_hierarchy_analyzer is None:
#         semantic_hierarchy_analyzer = SemanticHierarchyAnalyzer()
#     return json.dumps(semantic_hierarchy_analyzer.get_hierarchy_tags(word), ensure_ascii=False)


@app.route('/word2vec/<txt>/<int:topn>')
def word2vec(txt, topn):
    global word2vector
    if word2vector is None:
        word2vector = Word2Vector.get_word_model()
    words = txt.split()
    return json.dumps(word2vector.most_similar(words, topn=topn), ensure_ascii=False)


@app.route('/phrase2vec/<txt>/<int:topn>')
def phrase2vec(txt, topn):
    global phrase2vector
    if phrase2vector is None:
        phrase2vector = Word2Vector.get_phrase_model()
    words = txt.split() | where(lambda word: word in phrase2vector.vocab.keys)
    return json.dumps(phrase2vector.most_similar(words, topn=topn), ensure_ascii=False)


@app.route('/')
def index():
    with open(os.path.join(os.path.dirname(__file__), "index.html")) as index_file:
        return index_file.read()


def run(**kwargs):
    app.run(**kwargs)


if __name__ == '__main__':
    app.debug = True
    app.run(port=7000, host="0.0.0.0")