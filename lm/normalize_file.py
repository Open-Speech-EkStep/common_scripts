from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from indicnlp.tokenize.indic_tokenize import trivial_tokenize
import argparse
from tqdm import tqdm
from joblib import Parallel, delayed
def process(lang, sent):
    normalizer = IndicNormalizerFactory().get_normalizer(lang)
    normalized = normalizer.normalize(sent)
    processed = ' '.join(trivial_tokenize(normalized, lang))
    return processed

def normalize_file(lang, input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as in_fp, open(output_path, 'w', encoding='utf-8') as out_fp:
        lines = in_fp.read().splitlines()
        out = Parallel(n_jobs=-1)(delayed(process)(lang, i) for i in tqdm(lines))
        for line in out:
            out_fp.write(line)
            out_fp.write('\n')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run')
    parser.add_argument('--lang', '-l', type=str)
    parser.add_argument('--inp-file', '-i',type=str)
    parser.add_argument('--out-file', '-o',type=str)
    args_local = parser.parse_args()
    normalize_file(args_local.lang, args_local.inp_file, args_local.out_file)
