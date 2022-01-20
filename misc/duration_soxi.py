import sox
import glob
import numpy as np
import sys
from tqdm import tqdm
import os
from joblib import Parallel, delayed
import pandas as pd


def get_duration_single_file(local_file):
 
    duration = sox.file_info.duration(local_file)
    sample_rate = sox.file_info.sample_rate(local_file)
    channels = sox.file_info.channels(local_file)
    bitrate = sox.file_info.bitrate(local_file)

    clean_duration = 0    
    if 'clean' in local_file.split('/'):
        clean_duration = duration

    return {'file_name':local_file ,'duration': duration, 'sample_rate': sample_rate, 'channels': channels, 'bitrate': bitrate}

def get_duration(path_local, name):
    if not os.path.exists(path_local):
        raise Exception("Sorry this path doesn't exists")
    files = glob.glob(path_local + '/**/*.wav', recursive=True)
    print("Number of files present: ", len(files))
    total_seconds = pd.DataFrame(columns=['file_name','duration','sample_rate','channels', 'bitrate'])

    total_seconds = total_seconds.append( Parallel(n_jobs=24)( delayed(get_duration_single_file)(local_file) for local_file in tqdm(files)), ignore_index = True)

    #print(total_seconds)
    total_ = total_seconds.sum(axis=0,skipna = True)
 
    total_seconds.to_csv(name + '.csv', index=False)
    print('CSV file Generated!')

    #print(total_)
    print("Total Duration of Data in Hours: ", total_['duration']/3600)
    print("Unique Sample Rate values:", pd.unique(total_seconds['sample_rate']))
    print("Unique Channels values:", pd.unique(total_seconds['channels']))
    print("Unique Bitrate values:", pd.unique(total_seconds['bitrate']))

    #print("Total number of clean data in hours: ", total_[1]/3600)

if __name__ == "__main__":
    path = sys.argv[1]
    name = sys.argv[2]
    get_duration(path, name)
