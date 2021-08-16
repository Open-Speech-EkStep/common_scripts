from google.cloud import storage
import pandas as pd
from tqdm import tqdm

client = storage.Client()
bucket = client.get_bucket('ai4bharat')

audio_folder_name = 'data/maithili/mp3'
pdf_folder_name = 'data/maithili/pdf'

df = pd.read_csv('data/maithili/Maithili.csv')

audio_files = df['audio_path']
pdf_files = df['text_path']


def audio_prepare_file(file_path):

    file_name = file_path.split('/')[-1]

    return audio_folder_name + '/' + file_name


def pdf_prepare_file(file_path):

    file_name = file_path.split('/')[-1]

    return pdf_folder_name + '/' + file_name


for f in tqdm(pdf_files):
    blob = bucket.get_blob(f)
    blob.download_to_filename(pdf_prepare_file(f))

for f in tqdm(audio_files):
    blob = bucket.get_blob(f)
    blob.download_to_filename(audio_prepare_file(f))