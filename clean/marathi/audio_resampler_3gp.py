import subprocess
import glob
import os
from tqdm import tqdm
from joblib import Parallel, delayed
import sys

def resampler(input_file_path, output_folder_path):

    output_file_path = output_folder_path + input_file_path.split('/')[-1].replace('.3gp','.wav')

    command = (
        f"ffmpeg -hide_banner -loglevel panic -i {input_file_path} -ar 16000 -ac 1 -bits_per_raw_sample 16 -vn "
        f"{output_file_path}"
    )
    subprocess.call(command, shell=True)


if __name__ == '__main__':
  input_folder_path = sys.argv[1]
  files = glob.glob(input_folder_path + '/**/*.3gp', recursive=True)
  output_folder_path = input_folder_path + '_resampled/'
  if os.path.isdir(output_folder_path):
    print('Folder %s exists' % output_folder_path)
    exit()
  
  os.makedirs(output_folder_path)

  Parallel(n_jobs=24)( delayed(resampler)(local_file, output_folder_path) for local_file in tqdm(files))
