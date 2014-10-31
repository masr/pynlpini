#!/bin/bash -e

/usr/bin/python $SRC_BASE/pynlpini/seg/seg_file.py \
-i $BASE/data/word2vec.training.txt \
-o $BASE/tmp/word2vec.training_seg.txt

$BASE/../lib/word2vec-read-only/word2vec \
-train $BASE/tmp/word2vec.training_seg.txt \
-output $BASE/model/word2vec_word.word2vec.model \
-cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 1 -binary 1 -iter 20


$BASE/../lib/word2vec-read-only/word2phrase \
-train $BASE/tmp/word2vec.training_seg.txt \
-output $BASE/tmp/word2vec.training_seg_phrase0.txt \
-threshold 200 \
-min-count 2 \
-debug 2

/bin/cat $BASE/tmp/word2vec.training_seg_phrase0.txt | /usr/bin/tr -d "_" > $BASE/tmp/word2vec.training_seg_phrase0_tr.txt

$BASE/../lib/word2vec-read-only/word2phrase \
-train $BASE/tmp/word2vec.training_seg_phrase0_tr.txt \
-output $BASE/tmp/word2vec.training_seg_phrase1.txt \
-threshold 200 \
-min-count 2 \
-debug 2

/bin/cat $BASE/tmp/word2vec.training_seg_phrase1.txt | /usr/bin/tr -d "_" > $BASE/tmp/word2vec.training_seg_phrase1_tr.txt

$BASE/../lib/word2vec-read-only/word2vec \
-train $BASE/tmp/word2vec.training_seg_phrase1_tr.txt \
-output $BASE/model/word2vec_phrase.word2vec.model \
-cbow 1 -size 200 -window 5 -negative 25 -hs 0 -sample 1e-5 -threads 1 -binary 1 -iter 20 \


