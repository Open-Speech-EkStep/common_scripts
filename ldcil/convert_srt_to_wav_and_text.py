##Usage
##python convert_srt_to_wav_and_text.py -wav Above51/ -srt Fe_ABove51_srt/ -dest new_Fe_Above51/
import pysrt
from pydub import AudioSegment
import os
import re
import string
from glob import glob
from pathlib import Path
import argparse


def timestamp_to_ms(time):
    t = [int(i) for i in time.split(',')[0].split(':')]
    return int((t[0]*3600+t[1]*60+t[2])*1000 + int(time.split(',')[-1]))
    
def get_cleaned_text(original_text):
    pattern = '[.()\'-/\‘\’\;]+'
    clean_text = (re.sub(pattern, '', original_text)).strip()
    clean_text = re.sub('[%s]' % re.escape(string.punctuation), '', clean_text)
    return clean_text

def save_text_file(text, destination_file_path):
    with open(destination_file_path, mode='w+', encoding='utf-8') as f:
        print(text,sep='',file=f)


def crop_audio(source_file_path,start,end,destination_file_name):
    
    audio = AudioSegment.from_wav(source_file_path)
    cropped_audio = audio[start:end]
    cropped_audio.export(destination_file_name,format='wav')
    
def save_wav_and_text_chunks_from_srt(srt_file_obj,file_name,org_wav_file_name,destination_folder):
    for s in srt_file_obj:
        count = s.index
        file_name_chunk_wav = os.path.join(destination_folder,file_name.split('.')[0]+ '-'+str(count) + '.wav')
        file_name_chunk_text = os.path.join(destination_folder,file_name.split('.')[0]+ '-'+str(count) + '.txt')


        start = timestamp_to_ms(str(s.start))
        end = timestamp_to_ms(str(s.end))

        crop_audio(org_wav_file_name,start,end,file_name_chunk_wav)
        clean_text = get_cleaned_text(str(s.text))
        save_text_file(clean_text,file_name_chunk_text)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-srt', '--source-folder-srt', help='source folder srt')
    parser.add_argument('-wav', '--source-folder-wav', help='source_folder_wav')
    parser.add_argument('-dest', '--destination-folder', help='destination_folder')

    args = parser.parse_args()
        
    # source_folder_srt = 'Fe_ABove51_srt'
    # source_folder_wav = 'Above51'
    # destination_folder = 'Fe_Above_new_text'
    
    source_folder_srt = args.source_folder_srt
    source_folder_wav = args.source_folder_wav
    destination_folder = args.destination_folder
    print(destination_folder)
    
    os.makedirs(destination_folder,exist_ok = True)
    srt_files_list = [name for name in os.listdir(source_folder_srt) if '.srt' in name ]

    for file_name in srt_files_list:
        org_wav_file_name = os.path.join(source_folder_wav,file_name.split('.')[0]+ '.wav')
        srt_file_obj = pysrt.open(os.path.join(source_folder_srt,file_name))
        save_wav_and_text_chunks_from_srt(srt_file_obj,file_name,org_wav_file_name,destination_folder)
        
    print('*********Text and Wav files saved at {1}*********'.format(destination_folder))


