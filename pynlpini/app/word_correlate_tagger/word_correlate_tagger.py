from _collections import defaultdict
from pynlpini import Word2Vector
from pipe import select, sort, as_list
import os
import logging

logging.basicConfig(format='%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s', level=logging.INFO)

labelled_word_path = "../../../data/app/word_correlate_tagger/labelled_word.csv"
tag_list_path = "../../../data/app/word_correlate_tagger/tag.csv"
unlabelled_word_path = "../../../data/app/word_correlate_tagger/unlabelled_word.csv"
result_path = "../../../data/app/word_correlate_tagger/tag_result.csv"
model = Word2Vector.get_phrase_model()
vocabs = set(model.vocab.keys())
ktag_to_utags = defaultdict(set)

if os.path.exists(labelled_word_path):
    with open(labelled_word_path) as labelled_tag_file:
        logging.info("Processing " + labelled_word_path)
        for line in labelled_tag_file:
            line = line.strip().decode("utf-8")
            if len(line.split("\t")) == 2:
                utag = line.split("\t")[0]
                ktag = line.split("\t")[1]
                if utag in vocabs:
                    ktag_to_utags[ktag].add(utag)
if os.path.exists(tag_list_path):
    with open(tag_list_path) as tag_list_file:
        logging.info("Processing " + tag_list_path)
        for key in tag_list_file:
            key = key.strip().decode("utf-8")
            if key in vocabs:
                ktag_to_utags[key].add(key)

if len(ktag_to_utags) == 0:
    raise BaseException("Cannot find tag.csv or labelled_word.csv")

with open(unlabelled_word_path) as unlabelled_word_file:
    with open(result_path, "w") as result_file:
        for word in [line.strip().decode("utf-8") for line in unlabelled_word_file]:
            try:
                sim_tags_info = [(tag, model.n_similarity([word], ktag_to_utags[tag])) for tag in
                                 ktag_to_utags.keys()] | sort(
                    key=lambda tag_info: tag_info[1], reverse=True) | as_list
                sim_tags_info = [t[0] + "," + str(t[1]) for t in sim_tags_info[0:10]]
                output_line = "\t".join([word] + sim_tags_info)
                result_file.write(output_line.encode("utf-8") + "\n")
            except Exception, ex:
                logging.exception(ex)
                logging.warning("Cannot tag the word " + word)
