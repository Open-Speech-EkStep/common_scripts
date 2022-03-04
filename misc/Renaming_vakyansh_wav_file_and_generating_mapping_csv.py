from glob import glob
import os
from tqdm import tqdm
import pandas as pd
import os.path

wav_files = glob('vakyansh_data_without_numbers_21hrs/*.wav')

renamed_wav_names = []
original_wav_names = []

for i in tqdm(range (0,len(wav_files))):
    wav_file = wav_files[i]
    txt_file = wav_file.replace('.wav', '.txt')
    
    if os.path.exists(txt_file):

        wav_name = wav_file.split("/")[-1].split(".")[0]
        renamed_wav = wav_file.replace('vakyansh_data_without_numbers_21hrs', 'renamed_vakyansh_data_without_numbers_21hrs').replace(wav_name, str(i))
        
        original_wav_names.append(wav_file.split("/")[-1])
        renamed_wav_names.append(renamed_wav.split("/")[-1])
            
        txt_name = txt_file.split("/")[-1].split(".")[0]
        renamed_txt = txt_file.replace('vakyansh_data_without_numbers_21hrs', 'renamed_vakyansh_data_without_numbers_21hrs').replace(txt_name, str(i))
        
        os.rename(wav_file, renamed_wav)
        os.rename(txt_file, renamed_txt)
    
    else:
        print(txt_file, 'does not exists!')
        
mapping = set(zip(original_wav_names, renamed_wav_names))
df = pd.DataFrame(mapping, columns=['fileName','renamed']).sort_values(by='renamed')

df.to_csv('mapping.csv', encoding='utf-8', index = False)
print("DONE!")