# usage : python latency_check.py folder_path 10

from tqdm import tqdm
from bol.models import load_model
import soundfile as sf
from glob import glob
import numpy as np
import timeit
import sys

model = load_model("en-in-ts")
rtf_list = []
execution_time_list = []
audio_lenght_list = []
folder_path = sys.argv[1]
num_files = int(sys.argv[2])

def get_wav_length(f):
    return sf.SoundFile(f).frames / 16000


wav_files = glob(folder_path + '/*.wav')

for file in tqdm(wav_files[:num_files]):
    start = timeit.default_timer()
    model.predict(file, 'wav')

    stop = timeit.default_timer()
    execution_time = stop - start
    audio_length = get_wav_length(file)
    execution_time_list.append(execution_time)
    audio_lenght_list.append(audio_length)
    rtf_list.append(execution_time/audio_length)

print(f"mean execution time : {np.mean(execution_time_list)}")
print(f"mean rtf : {np.mean(rtf_list)}")
