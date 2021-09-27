
## Purpose: 
## 1. Resamples audios to 16000
## 2. Extract transcripted text from large transcription file which contains other administrative information
## 3. Multiplies text by 3 for folder where 3 times a single word has been spoken.

import glob
import os
from pathlib import Path
from tqdm import tqdm
import sys
from joblib import Parallel, delayed



def join_words(word_list):
    sentence=""
    for word in word_list:
        sentence += word.replace("\n"," ")
    return sentence.strip()

#txt_paths=list(Path(sys.argv[1]).glob("*.txt"))



def process_text_file(txt_file, destination_path):
    destination_dir = "/".join(destination_path.split('/')[:-1])
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)

    lines = []
    with open(txt_file,"r", encoding='utf8') as file:
        lines = file.readlines()

    hindi_text = join_words(lines[lines.index('RECORDED TEXT :: \n')+1 : lines.index('TEXT TRANSLITERATION :: \n')])
    
    three_times_repitition = ['Command_and_Control_Words-W1','Person_Name-W2', 'Place_Name-W2', 'Most_Frequent_Word-FullSet-W3B', 'Most_Frequent_Word-Part-W3A']

    for rep in three_times_repitition:
        if rep in destination_path:
            hindi_text_list = [hindi_text]*3
            hindi_text = " ".join(hindi_text_list)
            break;

    with open(destination_path, 'w+', encoding='utf8') as file:
        file.writelines(hindi_text)

def process_wav_file(wav_file, destination_path):
    command = f"ffmpeg -i {wav_file}  -ar 16000 -ac 1 -bits_per_raw_sample 16 {destination_path}"
    os.system(command)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("SYNTAX: python ldcil_extract_text.py <path to root input folder> <output folder path/name>")
        exit()

    print("Input Path")

    source_path = os.path.abspath(sys.argv[1])
    destination_path = os.path.abspath(sys.argv[2])

    txt_source_paths_wildcard = os.path.join(source_path, '**/*.txt')
    wav_source_paths_wildcard = os.path.join(source_path, '**/*.wav')


    txt_source_paths_list = glob.glob(txt_source_paths_wildcard, recursive=True)
    wav_source_paths_list = glob.glob(wav_source_paths_wildcard, recursive=True)


    print("** Number of Text files, ", len(txt_source_paths_list))
    print("** Number of Wav files, ", len(wav_source_paths_list))

    if not os.path.isdir(destination_path):
        os.makedirs(destination_path, exist_ok=True)
        print("** Creating Target Directory")

    Parallel(n_jobs=-1)( delayed(process_text_file)(txt_file_path_local, txt_file_path_local.replace(source_path, destination_path)) for txt_file_path_local in tqdm(txt_source_paths_list))
    print("** Text Files processing done, doing wav files now...")

    Parallel(n_jobs=1)( delayed(process_wav_file)(wav_file_path_local, wav_file_path_local.replace(source_path, destination_path)) for wav_file_path_local in tqdm(wav_source_paths_list))
    print("** Yipie, Wav Files processing done")