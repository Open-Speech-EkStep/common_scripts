# Usage -> python WadaSNR.py -i /path/to/folder/conatining/wav/files -w /path/to/wada/folder

import os, sys
import glob
import subprocess
import tempfile
import IPython
import soundfile as sf
import numpy as np
from tqdm import tqdm
import argparse

def compute_file_snr(file_path):
    """ Convert given file to required format with FFMPEG and process with WADA."""
    _, sr = sf.read(file_path)
    new_file = file_path.replace(".wav", "_tmp.wav")
    if sr != 16000:
        command = f'ffmpeg -i "{file_path}" -ac 1 -acodec pcm_s16le -y -ar 16000 "{new_file}"'
    else:
        command = f'cp "{file_path}" "{new_file}"'
    os.system(command)
    command = [f'"{WADA_PATH}/Exe/WADASNR"', f'-i "{new_file}"', f'-t "{WADA_PATH}/Exe/Alpha0.400000.txt"', '-ifmt mswav']
    output = subprocess.check_output(" ".join(command), shell=True)
    try:
        output = float(output.split()[-3].decode("utf-8"))
    except:
        raise RuntimeError(" ".join(command))
    os.system(f'rm "{new_file}"')
    return output, file_path

def main(inp_folder):
    wav_files = glob.glob(f"{inp_folder}/**/*.wav", recursive=True)
    print(f" > Number of wav files {len(wav_files)}")

    file_snrs = [None] * len(wav_files) 
    for idx, wav_file in tqdm(enumerate(wav_files)):
        tup = compute_file_snr(wav_file)
        file_snrs[idx] = tup

    snrs = [tup[0] for tup in file_snrs]

    error_idxs = np.where(np.isnan(snrs) == True)[0]

    file_snrs = [i for j, i in enumerate(file_snrs) if j not in error_idxs]
    file_names = [tup[1] for tup in file_snrs]
    snrs = [tup[0] for tup in file_snrs]
    file_idxs = np.argsort(snrs)

    with open('SNR_values.csv', 'w+') as file:
        file.write("file_path,snr_value")
        file.write("\n")
        for i in range(len(wav_files)):
            file_idx = file_idxs[i]
            file_name = file_names[file_idx]
            file.write(file_name+","+str(snrs[file_idx]))
            file.write("\n")

    print(f"\n\n\n > Average SNR of the dataset:{np.mean(snrs)}")
    print(f"\n To check snr values of each file open SNR_values.csv")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--inp-folder",
        help="input folder of wav files",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-w",
        "--wada-path",
        help="path to wada folder",
        type=str,
        required=True,
    )
    
    args = parser.parse_args()
    WADA_PATH = args.wada_path
    main(args.inp_folder)
