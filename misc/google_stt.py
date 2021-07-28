#Usage: python google_stt.py  --input raw/ --output-dir transcribed_stt/ --lang hi-IN --credentials /path_to_gcp_credentials.json_file
import glob
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
from tqdm import tqdm
import os
import sys
import pickle
from joblib import Parallel, delayed
import argparse


def sample_recognize(local_file_path, output_dir, language):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """


    filename = local_file_path.split('/')[-1][:-3] + 'txt'
    filepath_text =  os.path.join(output_dir,filename)

    # if continue_skip and os.path.exists(filepath_text):
    #     return

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = language

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,

        "audio_channel_count": 1,
        "enable_word_time_offsets": True,
        "enable_automatic_punctuation":False
    }

    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    #print("Starting Call")
    response = client.recognize(config, audio)


    #print("Call ended")
    transcript = ""
    if response:
        if response.results and response.results[0]:
            if response.results[0].alternatives and response.results[0].alternatives[0]:
                transcript = response.results[0].alternatives[0].transcript
   

    
    with open(filepath_text, 'w+', encoding='utf8') as file:
        file.write(transcript)


def call_STT_txt_parallel(input_dir, output_dir, language, jobs):
    files = glob.glob(f"{input_dir}/**/*.wav", recursive=True)
    print("** STT is going to run on ", len(files), " files")

    Parallel(n_jobs=jobs)(delayed(sample_recognize)(local_file, output_dir, language) for local_file in tqdm(files))    
    
    print("## STT has finished")




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--jobs', type=int, default=24)
    parser.add_argument('--lang', required=True)
    parser.add_argument('--resume', type=bool, default=False)
    parser.add_argument('--credentials', type=str, required=True, help="path to json file containing gcp credintials")
    args = parser.parse_args()

    # global continue_skip
    # continue_skip = args.resume
    print("** STT is going to run for ", args.lang, " language")
    os.makedirs(args.output_dir,exist_ok=True)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=args.credentials

    call_STT_txt_parallel(args.input, args.output_dir, args.lang, args.jobs)
