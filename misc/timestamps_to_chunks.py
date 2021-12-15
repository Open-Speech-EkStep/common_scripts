'''
# Extract Audio chunks using start & end time mentioned in given CSV file.

# Usage: python timestamps_to_chunks.py <CSV_FILE_PATH>
# Ex: python timestamps_to_chunks.py tts_modi_exp/pm_modi_food_and_agriculture.csv
'''

from pathlib import Path
from pydub import AudioSegment
import os
import pandas as pd
import sys

SOURCE_FOLDER = 'tts_modi_exp/resampled_22050Hz/'
DESTINATION_FOLDER = 'tts_modi_exp/nn/'

CSV_FILE_PATH = sys.argv[1]

def get_chunks_per_file(csv_file):
    wav_filename = csv_file.split('/')[-1].replace('.csv', '.wav')
    file_path = SOURCE_FOLDER + wav_filename
    print("File Path: ", file_path)
    df = pd.read_csv(csv_file)
    
    output_folder = DESTINATION_FOLDER + wav_filename.replace('.wav', '')
    print("Output Folder: ", output_folder)
    os.makedirs(output_folder, exist_ok=True)
    
    audio = AudioSegment.from_wav(os.path.join(file_path))
    
    for i in range(0, len(df)):
        # print("Start time: ", df['Start_time'][i] , "End time: ", df['End_time'][i])
    
        startSec = df['Start_time'][i]
        endSec = df['End_time'][i]

        startTime = startSec * 1000
        endTime = endSec * 1000

        newAudio = audio[startTime:endTime]
        newAudio_name = str(file_path).split('/')[-1][:-4] + "_chunk-" + str(i) + '.wav'
        
        # print(newAudio_name)
        # print(os.path.join(output_folder, newAudio_name))
        
        newAudio.export(os.path.join(output_folder, newAudio_name), format="wav")
        

get_chunks_per_file(CSV_FILE_PATH)
print("Chunking Done!")