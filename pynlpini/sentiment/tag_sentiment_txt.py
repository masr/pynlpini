# coding=utf-8
import os
from pynlpini.seg.seg_tagger import SegTagger
import pynlpini.common.ascii_processor as ap
import pynlpini.common.chinese_processor as cp
import json
from optparse import OptionParser
from pipe import *

RELATIVE_PARAMETER = 3


def normalize(txt):
    puncs = cp.CHINESE_PUNCS + ap.ASCII_PUNCS | where(lambda c: c not in u"?？!！~") | as_list

    def replace_char(c):
        if c in puncs:
            return "|"
        if c in cp.CHINESE_DIGITS + ap.ASCII_DIGITS:
            return '9'
        index = (cp.CHINESE_LOWER_LETTERS + cp.CHINESE_UPPER_LETTERS).find(c)
        if index != -1:
            return (ap.ASCII_LOWER_LETTERS + ap.ASCII_UPPER_LETTERS)[index].lower()
        if c in ap.ASCII_LOWER_LETTERS + ap.ASCII_UPPER_LETTERS:
            return c.lower()
        return c


    return ''.join(txt | select(replace_char))


def get_features(seged_txt):
    lines = seged_txt.split("\n")
    for line in lines:
        line = line.strip()
        line = normalize(line)
        sentences = line.split("|")
        for sentence in sentences:
            words = sentence.split()
            # words = words | where(lambda word: word not in STOP_WORD_SET) | as_list
            for i in range(len(words)):
                for j in range(0, RELATIVE_PARAMETER + 1):
                    start = i
                    end = i + j
                    if end >= len(words):
                        continue
                    yield '_'.join(words[start:end + 1])


def process_file(file_path, is_pos):
    global current_index
    with open(file_path) as file:
        content = file.read().strip().decode("utf-8")
        content = tagger.seg_as_txt(content)
        features = get_features(content) | as_list
        tmp_feature_file.write(content.encode("utf-8") + "\n")
        tmp_feature_file.write(" ".join(features).encode("utf-8"))
        tmp_feature_file.write("\n\n\n")
        feature_indexes = []
        for feature in features:
            if feature in feature_to_index_dict:
                feature_indexes.append(feature_to_index_dict[feature])
            else:
                feature_to_index_dict[feature] = current_index
                feature_indexes.append(current_index)
                current_index += 1
        feature_index_set = sorted(set(feature_indexes))
        label = "1" if is_pos else "0"
        feature_index_strs = feature_index_set | select(
            lambda index: str(index) + ":" + str(feature_indexes.count(index))) | as_list
        format_file.write(label + " " + ' '.join(feature_index_strs) + "\n")


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--pos_dir", action="store", dest="pos_dir", help="positive txt directories, separate by ;")
    parser.add_option("-n", "--neg_dir", action="store", dest="neg_dir", help="negative txt directories, separate by ;")
    parser.add_option("-s", "--svm_output", action="store", dest="svm_output_path",
                      help="svm format training output file path")
    parser.add_option("-i", "--index_output", action="store", dest="index_output_path",
                      help="feature index output file path")
    parser.add_option("-t", "--tmp_file", action="store", dest="tmp_file",
                      help="tmp file to store features of each record")

    options, args = parser.parse_args()
    pos_dirs = options.pos_dir.split(";")
    neg_dirs = options.neg_dir.split(";")
    tmp_feature_file_path = options.tmp_file
    output_svm_path = options.svm_output_path
    output_index_path = options.index_output_path

    tagger = SegTagger()
    feature_to_index_dict = dict()
    current_index = 1

    with open(output_svm_path, "w") as format_file:
        with open(output_index_path, "w") as index_file:
            with open(tmp_feature_file_path, "w") as tmp_feature_file:
                for pos_dir in pos_dirs:
                    file_names = os.listdir(pos_dir)
                    for file_name in file_names:
                        print "processing " + file_name
                        process_file(pos_dir + "/" + file_name, True)
                for neg_dir in neg_dirs:
                    file_names = os.listdir(neg_dir)
                    for file_name in file_names:
                        print "processing " + file_name
                        process_file(neg_dir + "/" + file_name, False)
                json.dump(feature_to_index_dict, index_file)

