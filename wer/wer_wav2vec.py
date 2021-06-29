
import pandas as pd
import numpy as np
import glob
import Levenshtein as Lev
from tqdm import tqdm
import swifter
import argparse
from components import compute_wer

def wer( s1, s2):
        """
        Computes the Word Error Rate, defined as the edit distance between the
        two provided sentences after tokenizing to words.
        Arguments:
            s1 (string): space-separated sentence
            s2 (string): space-separated sentence
        """

        # build mapping of words to integers
        b = set(s1.split() + s2.split())
        word2char = dict(zip(b, range(len(b))))

        # map the words to a char array (Levenshtein packages only accepts
        # strings)
        w1 = [chr(word2char[w]) for w in s1.split()]
        w2 = [chr(word2char[w]) for w in s2.split()]

        return Lev.distance(''.join(w1), ''.join(w2))

def cer(s1, s2):
    """
    Computes the Character Error Rate, defined as the edit distance.
    Arguments:
        s1 (string): space-separated sentence
        s2 (string): space-separated sentence
    """
    s1, s2, = s1.replace(' ', ''), s2.replace(' ', '')
    return Lev.distance(s1, s2)

def clean_text(row):
    return row[0][0:row.ind]

def preprocess(original_csv):
    original_csv['ind'] = original_csv['text'].str.index('(None')
    original_csv['cleaned_text'] = original_csv.swifter.apply(clean_text, axis = 1)
    return original_csv

def calculate_wer(row):
    wer_local = ''
    try:
        wer_local = wer(row['original'], row['predicted'])
        #cer_local = cer(row['cleaned_text'], row['text_y'])
    except:
        print(row)
        return len(row['original'].split(' '))
    return wer_local


def calculate_cer(row):
    try:
        cer_local = cer(row['original'], row['predicted'])
    except:
        return len(row['original'].str.replace(' ','').str.len())
    return cer_local


def calculate_errors(row):
    ret_object = compute_wer(predictions=[row['predicted']], references=[row['original']])
    return [ret_object['substitutions'], ret_object['insertions'], ret_object['deletions']]


def run_pipeline(ground_truth, predicted):
    
    with open(ground_truth, encoding='utf-8') as file:
        original_csv = file.readlines()
    
    original_csv = [line.strip() for line in original_csv]
    original_csv = pd.DataFrame(original_csv, columns=['text'])

    with open(predicted, encoding='utf-8') as file:
        predicted_csv = file.readlines()
 
    predicted_csv = [line.strip() for line in predicted_csv]
    predicted_csv = pd.DataFrame(predicted_csv, columns=['text'])


    original_csv = preprocess(original_csv)
    predicted_csv = preprocess(predicted_csv)


    df_merged = pd.DataFrame(data = [original_csv.cleaned_text.values, predicted_csv.cleaned_text.values],index=None)
    df_merged = df_merged.transpose()
    df_merged.columns = ['original', 'predicted']
    
    df_merged['wer'] = df_merged.apply(calculate_wer, axis = 1)
    df_merged['cer'] = df_merged.swifter.apply(calculate_cer, axis = 1)
    df_merged['num_tokens'] = df_merged['original'].str.split().str.len()
    df_merged['num_chars'] = df_merged['original'].str.replace(' ','').str.len()
    
    df_merged.sort_values(by = 'wer', ascending=False)
    fwer = df_merged.wer.sum() / df_merged.num_tokens.sum()
    fcer = df_merged.cer.sum() / df_merged.num_chars.sum()
    print('WER: ', fwer*100)
    print('CER: ', fcer*100)
    return df_merged
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process CER pipeline')
    parser.add_argument('-o', '--original', required=True, help='Original File')
    parser.add_argument('-p', '--predicted', required=True, help='Predicted File')
    parser.add_argument('-s', '--save-output', help='save output file', type=bool)
    parser.add_argument('-n', '--name', help='save output file name', type=str)
    parser.add_argument('-e', '--sid', type=bool)
    
    args_local = parser.parse_args()
    #print(args_local)
    df = run_pipeline(args_local.original, args_local.predicted)

    if args_local.sid:
        ret_object= df.swifter.apply(calculate_errors, axis=1)
        df['errors'] = ret_object
        df_errors = pd.DataFrame(df['errors'].to_list(), columns=['substitutions','insertions', 'deletions'])

        df = pd.concat([df, df_errors], axis=1)
        

    if args_local.save_output:
        df.to_csv(args_local.name, index=False)