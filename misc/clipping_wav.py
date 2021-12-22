'''
# Clip Audio by passing start & end time.

# Usage: python clipping_wav.py <WAV_PATH> <START_TIME_IN_SEC> <END_TIME_IN_SEC> 
# Ex: python clipping_wav.py audio.wav 5 1122
'''

from pathlib import Path
from pydub import AudioSegment
import os
import pandas as pd
import sys

DESTINATION_FOLDER = 'tts_modi_exp/new_data/again/clipped_wav_16kHz/'

WAV_PATH = sys.argv[1]
START_TIME = sys.argv[2]
END_TIME = sys.argv[3]

def get_chunks_per_file(wav, start_time, end_time):
    wav_filename = wav.split('/')[-1]
    print("Wav_filename: ", wav_filename)
    
    audio = AudioSegment.from_file(os.path.join(wav))
    
    startSec = int(start_time)
    endSec = int(end_time)

    startTime = startSec * 1000
    endTime = endSec * 1000

    newAudio = audio[startTime:endTime]
    newAudio_name = wav_filename
    
    print(newAudio_name)
    print(os.path.join(DESTINATION_FOLDER, newAudio_name))
    
    newAudio.export(os.path.join(DESTINATION_FOLDER, newAudio_name), format="wav")
        

get_chunks_per_file(WAV_PATH, START_TIME, END_TIME)
print("Clipping Done!")