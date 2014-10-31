#!/bin/bash

BASE=$(cd "$(dirname "$0")/";pwd)

wget http://www.dataini.com/projects/pynlpini/models/seg.crf.model $BASE/pynlpini/model/seg.crf.model
wget http://www.dataini.com/projects/pynlpini/models/pos.crf.model $BASE/pynlpini/model/pos.crf.model
wget http://www.dataini.com/projects/pynlpini/models/ner.crf.model $BASE/pynlpini/model/ner.crf.model
wget http://www.dataini.com/projects/pynlpini/models/semantic_tag.lst $BASE/pynlpini/model/semantic_tag.lst
wget http://www.dataini.com/projects/pynlpini/models/semantic_tree.lst $BASE/pynlpini/model/semantic_tree.lst
wget http://www.dataini.com/projects/pynlpini/models/sentiment.svm.model $BASE/pynlpini/model/sentiment.svm.model
wget http://www.dataini.com/projects/pynlpini/models/sentiment_feature_index.json $BASE/pynlpini/model/sentiment_feature_index.json
wget http://www.dataini.com/projects/pynlpini/models/word2vec.word2vec.model $BASE/pynlpini/model/word2vec.word2vec.model
wget http://www.dataini.com/projects/pynlpini/models/word2phrase.word2vec.model $BASE/pynlpini/model/word2phrase.word2vec.model

