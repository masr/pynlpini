# coding=utf-8
import re
import os

CHINESE_PUNCS = u"》』，〈％「）【＠※…（】！〇。」—；〉〕〔．　、‧？＋『《︰“”‘’：%￥#～·"
CHINESE_DIGITS = u"０１２３４５６７８９"
CHINESE_UPPER_LETTERS = u"ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
CHINESE_LOWER_LETTERS = u"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"

with open(os.path.join(os.path.dirname(__file__), "../dict/stop_word.csv")) as dict_file:
    STOP_WORD_SET = set([line.strip().decode("utf-8") for line in dict_file.readlines()])

with open(os.path.join(os.path.dirname(__file__), "../dict/simple_to_traditional.dict")) as dict_file:
    simple_line = dict_file.readline().strip().decode("utf-8")
    traditional_line = dict_file.readline().strip().decode("utf-8")
    tra2sim_dic = {}
    sim2tra_dic = {}
    for i in range(len(simple_line)):
        tra2sim_dic[traditional_line[i]] = simple_line[i]
        sim2tra_dic[simple_line[i]] = traditional_line[i]


def is_all_chinese(str_unicode):
    re_han = re.compile(ur"^([\u4E00-\u9FA5]+)$", re.U)
    return True if re_han.match(str_unicode) else False


def traditional2simplified(txt):
    line = ""
    for c in txt:
        if c in tra2sim_dic:
            line += tra2sim_dic[c]
        else:
            line += c
    return line


def simplified2traditional(txt):
    line = ""
    for c in txt:
        if c in sim2tra_dic:
            line += sim2tra_dic[c]
        else:
            line += c
    return line


if __name__ == "__main__":
    print is_all_chinese(u"我们")
    print is_all_chinese(u"我们22")

