# coding=utf-8
import re
import os

CHINESE_PUNCS = u"》』，〈％「）【＠※…（】！〇。」—；〉〕〔．　、‧？＋『《︰“”‘’：%￥#～·"
CHINESE_DIGITS = u"０１２３４５６７８９"
CHINESE_UPPER_LETTERS = u"ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
CHINESE_LOWER_LETTERS = u"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"


def is_all_chinese(str_unicode):
    re_han = re.compile(ur"^([\u4E00-\u9FA5]+)$", re.U)
    return True if re_han.match(str_unicode) else False


with open(os.path.join(os.path.dirname(__file__), "../dict/stop_word.csv")) as dict_file:
    STOP_WORD_SET = set([line.strip().decode("utf-8") for line in dict_file.readlines()])

if __name__ == "__main__":
    print is_all_chinese(u"我们")
    print is_all_chinese(u"我们22")

