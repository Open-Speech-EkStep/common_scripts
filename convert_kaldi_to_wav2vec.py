import glob
import pandas as pd

def get_dataframe(files_wav):
    df = pd.DataFrame(files_wav, columns=['file_path'])
    if 'IITM' in df.file_path.values[0]:
        df['folder_type'] = 'IITM'
    else:
        df['folder_type'] = 'NPTEL'
        
   
    
    
    df['file_id'] = df.file_path.str.split('/').str[-1].str.split('.').str[0]
    
    if 'NPTEL' in df.file_path.values[0]:
        df['file_id'] = df.file_path.str.split('/').str[-2] + '_' + df.file_path.str.split('/').str[-1].str.split('.').str[0]
    
    return df

files_wav = glob.glob('./raw/IITM*/**/*.wav', recursive=True)
df_iitm = get_dataframe(files_wav)

files_wav = glob.glob('./raw/NPTEL*/**/*.wav', recursive=True)
df_nptel = get_dataframe(files_wav)

df_train = pd.concat([df_iitm, df_nptel])
df_train = df_train.reset_index(drop=True)
df_processed = pd.read_csv('./interim/train_NPTEL_IITM.csv')
df_merged = pd.merge(df_train, df_processed, on='file_id')



## Exporting Audios

import os
import pandas as pd
from  pydub import AudioSegment
from joblib import Parallel, delayed
from tqdm import tqdm
import swifter

def crop_audio_file(source_file_path, start_time, end_time, destination_file_path):
    audio = AudioSegment.from_wav(source_file_path)
    start = start_time*1000.0
    end = end_time*1000.0
    cropped_audio = audio[start:end]
    cropped_audio.export(destination_file_path+'.wav',format='wav')


def save_audio_files(row):
    source_file_path = row.file_path_x
    start_time = row.start_time
    end_time = row.end_time
    
    destination_file_path = './processed/' + row['folder_type']+'/' + row['file_id']
    #print(destination_file_path)
    if not os.path.exists(str(destination_file_path)):
        os.makedirs(destination_file_path, exist_ok=True)
        
    destination_file = destination_file_path +'/' +row['segment_id']
    
    crop_audio_file(source_file_path, start_time, end_time, destination_file)

tqdm.pandas()

df_merged.progress_apply(save_audio_files, axis=1)
