#!/bin/bash -e

export BASE=$(cd "$(dirname "$0")";pwd)
export SRC_BASE=$(cd "$(dirname "$0")/../";pwd)
export PYTHONPATH=$SRC_BASE:$SRC_BASE/lib/libsvm-3.18/python

rm -f $BASE/model/*
rm -f $BASE/tmp/*

$BASE/test_seg.sh
$BASE/test_pos.sh
$BASE/test_ner.sh
$BASE/test_sentiment.sh
$BASE/test_word2vec.sh

/usr/bin/python $BASE/suite.py
