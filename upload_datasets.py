import os
import argparse

def upload(master_dir, destination_bucket):
    lst = ['google', 'ground_truth', 'wav_16']
    for item in lst:
        source = master_dir + '/' + item
        destination = destination_bucket + item + '.zip'
        zip_name = master_dir + '/' + item+'.zip'
        cmd_zip = f'zip -r {zip_name} {source}'

        cmd = f'gsutil -m cp -r {zip_name} {destination}'

        cmd_remove_zip = f'rm {zip_name}'

        os.system(cmd_zip)
        os.system(cmd)
        os.system(cmd_remove_zip)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--master-dir', type=str, required=True)
    parser.add_argument('--destination-bucket', type=str, required=True)
    
    args = parser.parse_args()
    upload(args.master_dir, args.destination_bucket)

