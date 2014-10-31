# coding=utf-8
import unittest
import os
from pynlpini import Word2Vector


class Word2VectorTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWord2vec(self):
        base_dir = os.path.dirname(__file__)
        word2vector = Word2Vector.get_word_model(
            os.path.join(base_dir, "./model/word2vec_word.word2vec.model"))
        words = word2vector.most_similar([u"香辣蟹"])
        self.assertEqual(words[0][0], u"椒盐")
        self.assertEqual(words[1][0], u"排档")
        self.assertEqual(len(words), 10)
        words = word2vector.most_similar([u"香辣蟹", u"啤酒"], topn=5)
        self.assertEqual(words[0][0], u"椒盐")
        self.assertEqual(words[1][0], u"菜品")
        self.assertEqual(len(words), 5)
        word = word2vector.doesnt_match([u"香辣蟹", u"啤酒", u"椒盐", u"地铁站"])
        self.assertEqual(word, u"地铁站")
        cos = word2vector.similarity(u"椒盐", u"香辣蟹")
        self.assertTrue(0.996437 > cos > 0.996436)
        res = word2vector.n_similarity([u"椒盐", u"香辣蟹"], [u"地铁站", u"出去"])
        self.assertTrue(0.980 < res < 0.981)

    def testPhrase2vec(self):
        base_dir = os.path.dirname(__file__)
        phrase2vector = Word2Vector.get_phrase_model(
            os.path.join(base_dir, "./model/word2vec_phrase.word2vec.model"))
        res = phrase2vector.most_similar([u"历史悠久", u"法国"])
        self.assertEqual(res[2][0], "halohalo")


if __name__ == "__main__":
    unittest.main()