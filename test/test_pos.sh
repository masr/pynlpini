#!/bin/bash -e

/usr/bin/python $SRC_BASE/pynlpini/pos/tag_pos_txt.py $BASE/data/pos_training.txt $BASE/tmp/pos_training.normalize.txt $BASE/tmp/pos_training.tag.txt

crf_learn -f 1 -m 50 -c 1.0 -p 1 $SRC_BASE/pynlpini/pos/pos.template $BASE/tmp/pos_training.tag.txt $BASE/model/pos.crf.model

