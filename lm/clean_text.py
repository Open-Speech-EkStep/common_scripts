## Usage: python clean_text.py --input /path/to/input/text/file --output /path/to/clean/text/file --dict /path/to/dict.ltr.txt
import re
import string
import argparse
from tqdm import tqdm
from joblib import Parallel, delayed

def get_clean_lines(line, pattern):
    '''
    Returns line if no foreign character other than pattern is present else returns empty string
    '''
    
    line = re.sub('[%s]' % re.escape(string.punctuation), ' ', line)
    line = line.replace('\u0964', '')
    if not re.search(pattern, line):
        return ' '.join([word.upper() for word in line.split() if word])
    else:
        return ''


def clean_text(inp, out, dict):
    '''
        Text cleaning to replace punctuations from sentences and then remove sentences containing foreign language characters.
    '''
    with open(inp, mode='r', encoding='utf-8') as inp_file, open(out, mode='w+', encoding='utf-8') as out_file:
        lines = inp_file.read().splitlines()
        dict_pattern = get_regex_from_dict(dict)
        pattern = '[^ '+dict_pattern+']+'

        out = Parallel(n_jobs=-1)(delayed(get_clean_lines)(i, pattern) for i in tqdm(lines))
        for line in out:
            if line != '':
                out_file.write(line)
                out_file.write('\n')

def get_regex_from_dict(dict):
    '''
    Returns a string of characters from dict.ltr.txt
    '''
    dict_path = dict
    with open(dict_path, encoding='UTF-8') as f:
        dict_lines = f.readlines()
    chars = ''.join([line.split()[0].strip() for line in dict_lines])
    return chars

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--output', '-o', type=str)
    parser.add_argument('--dict', '-d', default='../../data/finetuning/dict.ltr.txt', type=str)
    args = parser.parse_args()
    clean_text(args.input, args.output, args.dict)
