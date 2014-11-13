# coding=utf-8
import sys



if __name__ == "__main__":
    try:
        file1 = open(sys.argv[1], "r")
    except:
        print "result file is not specified, or open failed!"
        sys.exit()

    wc_of_test = 0
    wc_of_gold = 0
    wc_of_correct = 0
    flag = True

    for l in file1:
        if l == "\n":
            continue

        _, g, r = l.strip().split()

        if r != g:
            flag = False

        if r in ('E', 'S'):
            wc_of_test += 1
            if flag:
                wc_of_correct += 1
            flag = True

        if g in ('E', 'S'):
            wc_of_gold += 1

    print "WordCount from test result:", wc_of_test
    print "WordCount from golden data:", wc_of_gold
    print "WordCount of correct segs :", wc_of_correct

    P = wc_of_correct / float(wc_of_test)
    R = wc_of_correct / float(wc_of_gold)

    print "P = %f, R = %f, F-score = %f" % (P, R, (2 * P * R) / (P + R))