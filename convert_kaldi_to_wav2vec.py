import os
import pandas as pd
from  pydub import AudioSegment
from joblib import Parallel, delayed
from tqdm import tqdm
import swifter
import glob
import argparse


def read_segments_with_text(folder_name,  mode):

    segments = []
    with open(folder_name + '/segments.txt') as file_local:
        segments = file_local.readlines()
    segments = [seg.split(' ') for seg in segments]
    df_segment = pd.DataFrame(segments, columns = ['segment_id', 'file_id', 'start_time', 'end_time'])
    df_segment['end_time'] = df_segment['end_time'].str.strip()

    if mode=='train':
        text = []
        with open(folder_name +'/text.txt') as file_local:
            text = file_local.readlines()
        text= [local_text.replace('\t',' ') for local_text in text]
        text = [local_text.split(' ',1) for local_text in text]
        df_text = pd.DataFrame(text, columns = ['segment_id', 'transcription'])
        df_text['transcription'] = df_text['transcription'].str.strip() 

    wavscp = []
    with open(folder_name+'/wav.scp.txt') as file:
        wavscp = file.readlines()        
    wavscp = [utt.split('\t') for utt in wavscp]
    df_file_wav = pd.DataFrame(wavscp, columns =['file_id', 'file_path'])
    df_file_wav.file_path = df_file_wav.file_path.str.strip()

    if mode=='train':
        df_merged = pd.merge(df_segment, df_text, on='segment_id' )
        df_merged = pd.merge(df_merged, df_file_wav, on='file_id' )
    else:
        df_merged = pd.merge(df_segment, df_file_wav, on='file_id' )

    df_merged['start_time'] = df_merged['start_time'].astype('float32')
    df_merged['end_time'] = df_merged['end_time'].astype('float32')
    df_merged['duration'] = df_merged.end_time - df_merged.start_time
    print("Total Duration is ", df_merged.duration.sum() / 3600)

    return df_merged



def crop_audio_file(source_file_path, start_time, end_time, destination_file_path):
    audio = AudioSegment.from_wav(source_file_path)
    start = start_time*1000.0
    end = end_time*1000.0
    cropped_audio = audio[start:end]
    cropped_audio.export(destination_file_path+'.wav',format='wav')
    
def export_text_file(destination_file_path, text):
    with open(destination_file_path+'.txt', mode='w+') as file:
        file.writelines(text)

def save_audio_files(row):
    source_file_path = row.file_path_x
    start_time = row.start_time
    end_time = row.end_time
    destination_file_path = row['destination']
    text = row['transcription']

    if not os.path.exists(str(destination_file_path)):
        os.makedirs(destination_file_path, exist_ok=True)
        
    destination_file = row['destination'] +'/' +row['segment_id']    
    crop_audio_file(source_file_path, start_time, end_time, destination_file)
    export_text_file(destination_file, text)


def main(wav_folder_path, destination_folder_path, kaldi_files_path, mode):
    df_segment = read_segments_with_text(kaldi_files_path, mode)
    files_wav = glob.glob(wav_folder_path + '/**/*.wav', recursive=True)

    df_train = pd.DataFrame(files_wav, columns=['wav_path'])
    df_train['folder'] = df['wav_path'].str.split('/').str[-2]
    df_train['destination'] = destination_folder_path +'/' + df_train['folder'] 
    df_merged = pd.merge(df_train, df_segment, on='file_id')
    
    if mode=='test':
        df_merged['transcription'] = 'ABC'
    
    tqdm.pandas()
    df_merged.progress_apply(save_audio_files, axis=1)   



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wav_folder_path", default=None, type=str, help="Path to wav directory")
    parser.add_argument("-d", "--destination", default=None, type=str, help="Path to directory")
    parser.add_argument("-k", "--kaldi_path", default=None, type=str, help="Kaldi path")
    parser.add_argument("-m", "--mode", default='train', type=str, help="Mode to run script on")
    
    args = parser.parse_args()
    main(args.wav_folder_path, args.destination, args.kaldi_path, args.mode)
