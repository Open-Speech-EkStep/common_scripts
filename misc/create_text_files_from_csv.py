from glob import glob
import os

filenames = glob('Transcript/Devanagari/*.txt')

def create_text_files(filepath):
	with open(filepath, mode = 'r', encoding = 'UTF-8') as f:
		lines = f.readlines()

  	utterance_name =[line.split('\t')[0]+ '.txt' for line in lines]
    text = [line.split('\t')[-1].strip() for line in lines]
    print(utterance_name[0:5],text[0:5])

for file in filenames:
	folder_name = file.split('.')[0].split('/')[-1]
	print(folder_name)

	create_text_files(file, folder_name)