import yaml
import os
from clean_text import clean_text
from normalize_file import  normalize_file
from tokenize_file import tokenize
from remove_duplicate_lines import remove_duplicate
from make_lexicon import make_lexicon_lst_from_txt_file

class PrepareData:
    def __init__(self, lang, file_name, loc, dict_path) -> None:
        self.lang = lang
        self.file_name = file_name
        self.loc = loc
        self.dict_path = dict_path
    
    def run_pipeline(self):
        os.chdir(self.loc)
        
        if self.lang == 'hi':

            print("normalize file")
            normalized_file_name = self.file_name.split('.')[0] + '.norm.txt'
            normalize_file(self.lang, self.file_name, normalized_file_name)

            print("removing punctuation with single space and removing lines with foreign characters")
            clean_file_name = normalized_file_name.replace('.txt', '.clean.txt')
            clean_text(normalized_file_name, clean_file_name, self.dict_path)

            print("tokenizing file")
            tokenized_file_name = clean_file_name.replace('.txt', '.tok.txt')
            tokenize(clean_file_name, tokenized_file_name, self.lang)

            print("removing duplicate lines")
            unique_file_name = tokenized_file_name.replace('.txt', '.unique.txt')
            remove_duplicate(tokenized_file_name, unique_file_name)

        if self.lang == 'en':

            print("removing punctuation with single space and removing lines with foreign characters")
            clean_file_name = self.file_name.replace('.txt', '.clean.txt')
            clean_text(self.file_name, clean_file_name, self.dict_path)

            print("tokenizing file")
            tokenized_file_name = clean_file_name.replace('.txt', '.tok.txt')
            tokenize(clean_file_name, tokenized_file_name, self.lang)

            print("removing duplicate lines")
            unique_file_name = tokenized_file_name.replace('.txt', '.unique.txt')
            remove_duplicate(tokenized_file_name, unique_file_name)


        #print("creating lm.binary")
        #make_lm_cmd = f'python generate_lm.py --input_txt {unique_file_name} --output_dir {self.dst_folder} --top_k 500000 --kenlm_bins {self.kenlm_bin_path} --arpa_order 5 --max_arpa_memory "85%" --arpa_prune "0|0|1" --binary_a_bits 255 --binary_q_bits 8 --binary_type trie'
        #os.system(make_lm_cmd)
        
        #print("creating lexicon from vocab")
        # make_lexicon_lst_from_txt_file(dst + '/vocab-500000.txt', dst + '/lexicon.lst')
        
        print('completed')


if __name__ == '__main__':
    config = yaml.safe_load(open('config.yaml', 'r'))
    lang = config['Params']['Lang']
    file_name = config['Params']['File']
    loc = config['Params']['Loc']
    dict_path = config['Params']['Dict']
    PrepareData(lang, file_name, loc, dict_path).run_pipeline()
