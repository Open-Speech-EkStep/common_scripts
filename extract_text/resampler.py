import os
import parameters
from tqdm import tqdm
from glob import glob

mp3_folder_path = parameters.AUDIO_FOLDER_PATH
wav_folder_path = parameters.WAV_FOLDER_PATH

os.makedirs(wav_folder_path, exist_ok=True)

mp3_files = glob(mp3_folder_path + '/*.mp3')

for audio in tqdm(mp3_files):
    wav_file_name = wav_folder_path + '/' + audio.split('/')[-1].replace('.mp3', '.wav')

    cmd = "ffmpeg -i " + str(audio) + " -ar 16000 -ac 1 -bits_per_raw_sample 16 -vn " + str(wav_file_name)
    os.system(cmd)