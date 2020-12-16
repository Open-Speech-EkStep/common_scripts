import sox
import glob
import numpy as np
import sys
from tqdm import tqdm
import os
from joblib import Parallel, delayed

def get_duration_single_file(file):
    return sox.file_info.duration(file)

def get_duration(path_local):
    if not os.path.exists(path_local):
        raise Exception("Sorry this path doesn't exists")
    files = glob.glob(path_local + '/*.wav')
    print("Number of files present: ", len(files))
    total_seconds = []

    total_seconds.extend( Parallel(n_jobs=-1)( delayed(get_duration_single_file)(local_file) for local_file in tqdm(files) ) )
    
    print("Total number of data in hours: ", np.sum(total_seconds)/3600)

if __name__ == "__main__":
    path = sys.argv[1]
    get_duration(path)