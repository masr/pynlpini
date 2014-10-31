import unittest
import test_seg
import test_pos
import test_ner
import test_impression
import test_sentiment
import test_word2vec
import test_semantic_tag
import test_semantic_hierarchy


def test(test_case):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    unittest.TextTestRunner(verbosity=2).run(suite)


test(test_seg.SegTaggerTestCase)
test(test_pos.PosTaggerTestCase)
test(test_ner.NerTaggerTestCase)
test(test_impression.ImpressionExtractorTestCase)
test(test_sentiment.SentimentClassifierTestCase)
test(test_word2vec.Word2VectorTestCase)
test(test_semantic_tag.SemanticTagTestCase)
test(test_semantic_hierarchy.SemanticHierarchyTestCase)

