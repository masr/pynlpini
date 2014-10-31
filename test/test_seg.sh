#!/bin/bash -e

/usr/bin/python $SRC_BASE/pynlpini/seg/tag_seg_txt.py $BASE/data/seg_training.txt $BASE/tmp/seg_training.normalize.txt $BASE/tmp/seg_training.tag.txt

crf_learn -m 50 -c 1.0 -p 1 $SRC_BASE/pynlpini/seg/seg.template $BASE/tmp/seg_training.tag.txt $BASE/model/seg.crf.model

