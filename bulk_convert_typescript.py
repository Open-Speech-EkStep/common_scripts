import os
from tqdm import tqdm
from convert_hf import *

list_models = ['Harveenchadha/vakyansh-wav2vec2-hindi-him-4200',
'Harveenchadha/vakyansh-wav2vec2-punjabi-pam-10',
'Harveenchadha/vakyansh-wav2vec2-urdu-urm-60',
'Harveenchadha/vakyansh-wav2vec2-sanskrit-sam-60',
'Harveenchadha/vakyansh-wav2vec2-odia-orm-100',
'Harveenchadha/vakyansh-wav2vec2-marathi-mrm-100',
'Harveenchadha/vakyansh-wav2vec2-malayalam-mlm-8',
'Harveenchadha/vakyansh-wav2vec2-maithili-maim-50',
'Harveenchadha/vakyansh-wav2vec2-dogri-doi-55',
'Harveenchadha/vakyansh-wav2vec2-bhojpuri-bhom-60',
'Harveenchadha/vakyansh-wav2vec2-assamese-asm-8',
'Harveenchadha/vakyansh-wav2vec2-tamil-tam-250',
'Harveenchadha/vakyansh-wav2vec2-telugu-tem-100',
'Harveenchadha/vakyansh-wav2vec2-nepali-nem-130',
'Harveenchadha/vakyansh-wav2vec2-kannada-knm-560',
'Harveenchadha/vakyansh-wav2vec2-gujarati-gnm-100',
'Harveenchadha/vakyansh-wav2vec2-indian-english-enm-700',
'Harveenchadha/vakyansh-wav2vec2-bengali-bnm-200'
]
#with open("model_names.txt") as file:
#    list_models = file.readlines()
    
for model in tqdm(list_models):
    language_name = model.split('/')[-1].split('-')[2]
    print(f"Currently working on {language_name}")
    output_dir = f'../../checkpoints/ts/{language_name}'
    os.makedirs(output_dir, exist_ok=True)
    convert_model(model, output_dir)
    os.system(f'zip -r {output_dir}/{language_name}.zip {output_dir}/')
