# coding=utf-8
import os
from pynlpini.lib.gensim import word2vec


class Word2Vector:
    @staticmethod
    def get_word_model(model_path=None, **kwargs):
        if model_path is None:
            base_dir = os.path.dirname(__file__)
            model_path = os.path.join(base_dir, "./../model/word2vec.word2vec.model")
        if "binary" in kwargs:
            binary = kwargs['binary']
        else:
            binary = True
        return word2vec.Word2Vec.load_word2vec_format(model_path, binary=binary)

    @staticmethod
    def get_phrase_model(model_path=None, **kwargs):
        if model_path is None:
            base_dir = os.path.dirname(__file__)
            model_path = os.path.join(base_dir, "./../model/phrase2vec.word2vec.model")
        return Word2Vector.get_word_model(model_path, **kwargs)