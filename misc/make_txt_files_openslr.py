import os
from tqdm import tqdm
import sys
import pandas as pd
def make_txt_from(dir_to_tsv, txts_destination_dir):
    #all_files = os.listdir(dir_to_tsv)
    #text_index_file = [i for i in all_files if '.tsv' in i]
    #assertEqual(len(text_index_file), 1)
    text_index_file = os.path.join(dir_to_tsv, 'line_index.tsv')
    file_tsv_df = pd.read_csv(text_index_file, delimiter='\t', header=None)
    for index, file in tqdm(enumerate(file_tsv_df[0])):
    	txt_file = str(file)+'.txt'

    	with open(os.path.join(txts_destination_dir, txt_file), 'w+') as f:
            f.write(str(file_tsv_df[1][index]))

if __name__ == "__main__":
    dir_to_tsv = sys.argv[1] #directory to line_index.tsv
    txts_destination_dir = sys.argv[2] #destinationn directory
    make_txt_from(dir_to_tsv, txts_destination_dir)
