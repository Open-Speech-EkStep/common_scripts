import os
from tqdm import tqdm
from pathlib import Path
from create_data import start_processing
from joblib import Parallel, delayed
import numpy as np

SOURCE_ROOT_FOLDER_PATH = "/home/jupyter/kannada2"
DESTINATION_ROOT_FOLDER_PATH = "/home/jupyter/kannada_pretrain"
NUM_WORKERS = -1


SOURCE_ROOT_FOLDER_PATH = os.path.abspath(SOURCE_ROOT_FOLDER_PATH)
DESTINATION_ROOT_FOLDER_PATH = os.path.abspath(DESTINATION_ROOT_FOLDER_PATH)

if not os.path.isdir(DESTINATION_ROOT_FOLDER_PATH):
	os.makedirs(DESTINATION_ROOT_FOLDER_PATH, exists_ok=True)

# Find all wav files in source folder

audio_paths = list(Path(SOURCE_ROOT_FOLDER_PATH).glob("**/clean/*.wav"))

# Get unique leaf level directiories in which wav files are present


source_dir_structure = list(set(["/"+os.path.join(*(path).split("/")[:-1]) for str(path) in audio_paths]))


#print(source_dir_structure)

# Parallelised data creation

total_time = Parallel(n_jobs=NUM_WORKERS)(delayed(start_processing)(source_dir_path,source_dir_path.replace(SOURCE_ROOT_FOLDER_PATH,DESTINATION_ROOT_FOLDER_PATH)) for source_dir_path in tqdm(source_dir_structure))
#print("Total time is ", np.sum(total_time)/3600)
