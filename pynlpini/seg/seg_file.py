from seg_tagger import SegTagger
from optparse import OptionParser


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input_file", action="store", dest="input_file", help="input file")
    parser.add_option("-o", "--output_file", action="store", dest="output_file", help="output file")
    parser.add_option("-m", "--model_path", action="store", dest="model_path",
                      help="model path")
    parser.add_option("-a", "--model_args", action="store", dest="model_args",
                      help="model args")

    options, args = parser.parse_args()
    input_file_path = options.input_file
    output_file_path = options.output_file
    model_path = options.model_path
    model_args = options.model_args

with open(input_file_path) as input_file:
    with open(output_file_path, "w") as output_file:
        tagger = SegTagger(model_path, model_args)
        for line in input_file:
            line = tagger.seg_as_txt(line.decode("utf-8"))
            output_file.write(line.encode("utf-8"))


