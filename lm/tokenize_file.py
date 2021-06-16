import argparse

import sys
from tqdm import tqdm
from spacy.tokenizer import Tokenizer

def tokenize(inp, out, lang):
    if lang == 'hi':
        from spacy.lang.hi import Hindi
        nlp = Hindi()
    if lang == 'en':
        from spacy.lang.en import English
        nlp = English()

    tokenizer = Tokenizer(nlp.vocab)

    with open(inp, 'r', encoding='utf-8') as in_file:
        inp_lines = in_file.read().splitlines()

    out_file=open(out, 'w+', encoding='utf-8')

    for line in tqdm(inp_lines):
        tok_text = tokenizer(line)
        tok_list = [str(i) for i in list(tok_text)]
        t = " ".join(tok_list).split()
        out_line = " ".join(t)
        print(out_line, file=out_file)

    out_file.close()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--output', '-o', type=str)
    parser.add_argument('--lang', '-l', type=str)
    args = parser.parse_args()
    tokenize(args.input, args.output, args.lang)
