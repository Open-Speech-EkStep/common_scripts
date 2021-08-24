import os

from google.cloud import storage
import pandas as pd
from tqdm import tqdm

client = storage.Client()
bucket = client.get_bucket('ai4bharat')

audio_folder_name = 'data/konkani/mp3'
pdf_folder_name = 'data/konkani/pdf'

os.makedirs(audio_folder_name, exist_ok=True)
os.makedirs(pdf_folder_name, exist_ok=True)

df = pd.read_csv('data/konkani/Konkani.csv')

print("Number of records: ", len(df))

df = df[~df.duplicated(['text_path'], keep=False)]
df = df[~df.duplicated(['audio_path'], keep=False)]

audio_files = df['audio_path']
pdf_files = df['text_path']

print("Number of records after removing duplicates: ", len(df))


def audio_prepare_file(file_path):

    file_name = file_path.split('/')[-1]

    return audio_folder_name + '/' + file_name


def pdf_prepare_file(file_path):

    file_name = file_path.split('/')[-1]

    return pdf_folder_name + '/' + file_name


for f in tqdm(pdf_files):
    blob = bucket.blob(f)
    blob.download_to_filename(pdf_prepare_file(f))

for f in tqdm(audio_files):
    blob = bucket.blob(f)
    blob.download_to_filename(audio_prepare_file(f))