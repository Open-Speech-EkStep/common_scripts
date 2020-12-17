# Aman_Tiwari
# code to concatenate audio files to create training files for wav2vec2
# to run syntax is: python create_data.py <path to source> <path to destination>

import os
import sys
import glob
import random
import subprocess
from tqdm import tqdm
from pathlib import Path
from pydub import AudioSegment
from joblib import Parallel, delayed


def combine_wav_and_text(wav_list,file_path,file_name):
    if not os.path.isdir(file_path):
        os.makedirs(file_path,exist_ok=True)
    combined_wav=AudioSegment.silent(duration=0)
    # text=[]
    for file in wav_list:
        wav_path=file
        # txt_path=file.replace(".wav",".txt")
        combined_wav+= AudioSegment.from_wav(wav_path)
        # text.append(open(txt_path,"r",encoding="utf-8").readline())
    combined_wav.export(os.path.join(file_path,file_name+".wav"), format="wav")
    # final_text=" ".join(text)
    # with open(os.path.join(file_path,file_name+".txt"),"w",encoding="utf-8") as file:
    #     file.write(final_text)

def req_dur(file):
    command = f"soxi -D {file}"
    time = subprocess.check_output(command, shell=True)
    time = time.decode("utf-8").split('\n')[0]
    return time

def sanitize(audio_paths):
    failed=open("Files_not_found.txt","a+")
    new_audio_paths=[]
    for wav_path in audio_paths:
        wav=str(wav_path)
        txt=wav.replace("wav","txt")
        if not os.path.isfile(txt):
            print(txt,file=failed)
        else:
            new_audio_paths.append(wav_path)
    return new_audio_paths

def calculate_time(target_folder, num_workers=-1):
    total_time = []
    audio_paths = sorted(list(Path(target_folder).glob("**/*.wav")))
    # audio_paths = sanitize(audio_paths)
    # print("Total_files: ", len(audio_paths))
    total_time = Parallel(n_jobs=num_workers)(delayed(req_dur)(file) for file in audio_paths)
    total_time = [float(i) for i in total_time if i != ""]
    # print(sum(total_time) / 3600, " hrs")
    audio_paths=[str(path) for path in audio_paths]
    return total_time,audio_paths


# def calculate_time(path):
#     print("Calculating time of each file in old path to process.....")
#     total_time = []
#     files_after_cutting = glob.glob(os.path.join(path + "/*.wav"))
#     for file in tqdm(files_after_cutting):
#         command = f"soxi -D {file}"
#         time = subprocess.check_output(command, shell=True)
#         total_time.extend((time.decode("utf-8").split('\n')))
#     total_time = [float(i) for i in total_time if i!=""]
#     print(sum(total_time)/3600)
#     return total_time,files_after_cutting


def get_valid_permissible_files(total_time,files_after_cutting):
    # print("Selecting valid files...")
    files=[]
    time=[]
    for i in range(len(total_time)):
        if(total_time[i]<=30):
            files.append(files_after_cutting[i])
            time.append(total_time[i])
    return time,files

def get_merged_files_and_their_time(time,files):
    # print("Processing the files to get new possible files...")
    temp_time=time.copy()
    temp_file=files.copy()
    main_time=[]
    new_time=[]
    main_files=[]
    t=[]
    f=[]
    while temp_time:
        a=[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
        r=random.choice(a)
        if sum(t)<r and (sum(t)+temp_time[0])<=30:
            t.append(temp_time[0])
            f.append(temp_file[0])
            temp_time.pop(0)
            temp_file.pop(0)
        else:
            main_time.append(t)
            main_files.append(f)
            new_time.append(sum(t))
            t=[]
            f=[]  
    # print(f"Old number of files {len(time)}\nNew number of files {len(new_time)}")
    return new_time,main_files

def create_data(time,main_files,new_path):
    # print("creating data now....")
    count=0
    file_name="chunk"
    for i in main_files:
        combine_wav_and_text(i,new_path,file_name+str(count))
        count+=1
    # print(f"New files created in {new_path}")
    return time

def start_processing(path,new_path):
    time,files=calculate_time(path)
    time,files=get_valid_permissible_files(time,files)
    time,files=get_merged_files_and_their_time(time,files)
    new_files_time=create_data(time,files,new_path)
    return new_files_time
# new_train_time=start(sys.argv[1],sys.argv[2])
