from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
import argparse

def process(lang, sent):
    normalizer = IndicNormalizerFactory().get_normalizer(lang)
    return normalizer.normalize(sent)

def normalize_file(lang, input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as in_fp, open(output_path, 'w', encoding='utf-8') as out_fp:
        for line in in_fp.readlines():
            sent = line.rstrip('\n')
            out_fp.write(process(lang, sent))
            out_fp.write('\n')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run')
    parser.add_argument('--lang', '-l', type=str)
    parser.add_argument('--inp-file', '-i',type=str)
    parser.add_argument('--out-file', '-o',type=str)
    args_local = parser.parse_args()
    normalize_file(args_local.lang, args_local.inp_file, args_local.out_file)
