#!/bin/bash -e

/usr/bin/python $SRC_BASE/pynlpini/sentiment/tag_sentiment_txt.py \
-p "$BASE/data/sentiment/pos;$BASE/data/sentiment/pos1" \
-n "$BASE/data/sentiment/neg;$BASE/data/sentiment/neg1" \
-t $BASE/tmp/sentiment_training.tmp_features.txt \
-i $BASE/model/sentiment_feature_index.json \
-s $BASE/tmp/sentiment_training.tag.txt

$SRC_BASE/lib/libsvm-3.18/svm-train -t 0 $BASE/tmp/sentiment_training.tag.txt $BASE/model/sentiment.svm.model
