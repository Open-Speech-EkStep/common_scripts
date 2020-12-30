import json
from tqdm import tqdm
import glob

files = glob.glob('*.json')

#local_dict = json.loads(files[0])


for file in tqdm(files):
    with open(file) as f:
        data = json.load(f)
        url = data['webpage_url'] 
        with open('result.txt', 'a+') as local_file:
            print(url, file=local_file)


### youtube dl command:


'''
 youtube-dl --ignore-errors --write-info-json --skip-download -o "./%(playlist)s/%(title)s.%(ext)s" https://www.youtube.com/playlist?list=PLcBVsra3A46pi4ahQm5391M64_piHdJlK
'''