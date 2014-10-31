# coding=utf-8
import sys
import pynlpini.common.ascii_processor as ap
import pynlpini.common.chinese_processor as cp
from pipe import *


def normalize(txt):
    def replace_char(c):
        if c in cp.CHINESE_PUNCS + ap.ASCII_PUNCS:
            return "|"
        if c in cp.CHINESE_DIGITS + ap.ASCII_DIGITS:
            return '9'
        if c in cp.CHINESE_LOWER_LETTERS + cp.CHINESE_UPPER_LETTERS + ap.ASCII_LOWER_LETTERS + ap.ASCII_UPPER_LETTERS:
            return 'a'
        return c


    return ''.join(txt | select(replace_char))


def tag(raw_file_path, normalize_file_path, tag_file_path):
    with open(raw_file_path) as raw_file:
        with open(normalize_file_path, "w") as normalize_file:
            for line in raw_file:
                line = line.decode("utf-8").strip()
                line = normalize(line)
                normalize_file.write(line.encode("utf-8") + "\n")

    with  open(normalize_file_path) as normalize_file:
        with open(tag_file_path, "w") as tag_file:
            for line in normalize_file:
                line = line.decode("utf-8").strip()
                if len(line) == 0:
                    continue
                words = line.split()
                for word in words:
                    length = len(word)
                    if length == 1:
                        tag_file.write(word[0].encode("utf-8") + " S\n")
                    else:
                        if length > 1:
                            tag_file.write(word[0].encode("utf-8") + " B\n")
                            for i in range(1, length - 1):
                                tag_file.write(word[i].encode("utf-8") + " M\n")
                            tag_file.write(word[-1].encode("utf-8") + " E\n")
                        else:
                            continue
                tag_file.write("\n")


if __name__ == '__main__':
    tag(sys.argv[1], sys.argv[2], sys.argv[3])

