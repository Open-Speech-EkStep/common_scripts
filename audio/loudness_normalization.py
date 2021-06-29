from pydub import AudioSegment, effects
import glob
import os
from tqdm import tqdm

class AudioNormalization:
    def __init__(self, wav_file):
        self.wav_file = wav_file

    def loudness_normalization(self, target_dBFS=-15):
        audio_file = AudioSegment.from_file(self.wav_file, format='wav')
        loudness_difference = target_dBFS - audio_file.dBFS
        normalized_audio = audio_file + loudness_difference
        return normalized_audio

    def loudness_normalization_effects(self):
        audio_file = AudioSegment.from_file(self.wav_file, format='wav')
        normalized_audio = effects.normalize(audio_file)
        return normalized_audio

def rectify_audio_path(path):
    if path[-1] == "/":
        path = path[:-1]
    return path

def normalize_loudness(input, output):
    input_audio_path = rectify_audio_path(input)
    audio_dump_path = rectify_audio_path(output)
    audio_files = glob.glob(input_audio_path + '/**/*.wav', recursive=True)
    print("Normalization will run on ", len(audio_files))

    output_folder_path = audio_dump_path + '/' + input_audio_path.split('/')[-1] + '_loud_norm'
    os.makedirs(output_folder_path)
    
    for audio in tqdm(audio_files):
        normalized_audio = AudioNormalization(audio).loudness_normalization_effects()
        output_file_name = (output_folder_path + '/' +
                            audio.split('/')[-1])
        normalized_audio.export(output_file_name, format='wav')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Normalize')
    parser.add_argument('-i', '--input', required=True, help='Input path')
    parser.add_argument('-o', '--output', required=True, help='Output path')
    
    args_local = parser.parse_args()
    normalize_loudness(args_local.input, args_local.output)        
