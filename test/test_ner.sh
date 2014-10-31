#!/bin/bash -e

/usr/bin/python $SRC_BASE/pynlpini/ner/tag_ner_txt.py $BASE/data/ner_training.txt $BASE/tmp/ner_training.normalize.txt $BASE/tmp/ner_training.tag.txt

crf_learn -f 1 -m 50 -c 1.0 -p 1 $SRC_BASE/pynlpini/ner/ner.template $BASE/tmp/ner_training.tag.txt $BASE/model/ner.crf.model

