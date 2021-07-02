import re
import string
import argparse
import os

import sox

from tqdm import tqdm
from joblib import Parallel, delayed
from glob import glob

def get_clean_lines(line, pattern):
    
    '''
    Returns line if no foreign character other than pattern is present else returns empty string
    '''
    
    line = re.sub('[%s]' % re.escape("!\"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~"), '', line)
    
    if not re.search(pattern, line):
        return ' '.join([word.upper() for word in line.split() if word])
    else:
        return ''
    
def read_text_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        return f.read()
    
def write_text_file(line, fpath):
    with open(fpath, 'w+', encoding='utf-8') as f:
        return f.write(line)

def copy_file(src, dst):
    copy_cmd = 'cp ' + src + ' ' + dst
    os.system(copy_cmd)
    
def get_duration(fpath):
    return sox.file_info.duration(fpath)

def process_text_file(fpath, dst_txt_path, pattern):
    sentence = read_text_file(fpath)
    cleaned_sentence = get_clean_lines(sentence, pattern)
    
    dst_folder = '/'.join(dst_txt_path.split('/')[:-1])
    
    os.makedirs(dst_folder, exist_ok=True)
    
    if not cleaned_sentence == '':
        
        write_text_file(cleaned_sentence, dst_txt_path)
        copy_file(fpath.replace('.txt', '.wav'), dst_txt_path.replace('.txt', '.wav'))
        
        return 0
        
    else:
        return get_duration(fpath.replace('.txt', '.wav'))
        

def get_file_list(inp_folder):
    return glob(inp_folder+'/**/*.txt', recursive=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', '-i', type=str)
    parser.add_argument('--output-folder', '-o', type=str)
    args = parser.parse_args()
    
    txt_file_list = get_file_list(args.input_folder)
        
    pattern = "[^ 'A-Z]+"
    
    duration_rejected = Parallel(n_jobs=-1)(delayed(process_text_file)(fpath, fpath.replace(args.input_folder, args.output_folder), pattern) for fpath in tqdm(txt_file_list))
    
    print(f"Duration rejected {sum(duration_rejected)/3600:.3f} Hours")
