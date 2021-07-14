import pandas as pd
import argparse


def clean_text(row):
    return row[0][0:row.ind]

def get_number(row):
    return row[0][row.ind + 6:row.indx_end]

def preprocess(original_csv):
    original_csv['ind'] = original_csv['text'].str.index('(None')
    original_csv['indx_end'] = original_csv['text'].str.len() -1
    original_csv['cleaned_text'] = original_csv.apply(clean_text, axis = 1)
    original_csv['index'] = original_csv.apply(get_number, axis = 1)

    return original_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process CER pipeline')
    parser.add_argument('-t', '--tsv', required=True, help='Original File')
    parser.add_argument('-p', '--predicted', required=True, help='Predicted File')
    parser.add_argument('-n', '--name', help='save output file name', type=str)
    
    args_local = parser.parse_args()
    
    preds = []
    with open(args_local.predicted) as pred_file:
        preds= pred_file.readlines()

    preds = [pred.strip() for pred in preds]

    df = pd.DataFrame(preds)
    df.columns = ['text']
    df = preprocess(df)
    df_tsv = pd.read_csv(args_local.tsv, sep='\t')
    df_tsv = df_tsv.reset_index()
    df_tsv.columns = ['file_path', 'frame_length']
    df_tsv['utterance_id'] = df_tsv.file_path.str.split('/').str[-1].str.split('.').str[0]
    
    #print(df.head())

    with open(args_local.name, mode='w+') as file:
        for text, index in zip(df['cleaned_text'].values, df['index'].values):
                #print(index)
                print(df_tsv.loc[int(index)].utterance_id," ", text.strip(), file=file)
