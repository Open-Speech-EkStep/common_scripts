import parameters
from aeneas.executetask import ExecuteTask
from aeneas.language import Language
from aeneas.syncmap import SyncMapFormat
from aeneas.task import Task
from aeneas.task import TaskConfiguration
from aeneas.textfile import TextFileFormat
import aeneas.globalconstants as gc
import pandas as pd
from tqdm import tqdm
import os


class ForcedAlignment:
    def __init__(self, audio_file_path, txt_file_path):
        self.audio_file_path = audio_file_path
        self.txt_file_path = txt_file_path

    def align_audio_and_text(self, file_path):
        #config = TaskConfiguration()
        #cmd = "python - m aeneas.tools.execute_task " + str(self.audio_file_path) + " " + str(self.align_audio_and_text) + " task_language=asm|os_task_file_format=json|is_text_type=plain " + str(file_path) + " -r = \"tts=espeak-ng\""
        cmd = "bash test_aeneas.sh " + str(self.audio_file_path) + " " + str(self.txt_file_path) + " " + str(file_path)
        #config_string = "task_language = asm \ -r tts=espeak-ng|allow_unlisted_languages=True"
        #config[gc.PPN_TASK_LANGUAGE] = Language.ASM
        #config[gc.PPN_TASK_IS_TEXT_FILE_FORMAT] = TextFileFormat.PLAIN
        #config[gc.PPN_TASK_OS_FILE_FORMAT] = SyncMapFormat.JSON
        #task = Task(config_string=config_string)
        #task = Task()
        #task.configuration = config

        #task.audio_file_path_absolute = self.audio_file_path
        #task.text_file_path_absolute = self.txt_file_path
        #task.sync_map_file_path_absolute = file_path
        #ExecuteTask(task).execute()
        #task.output_sync_map_file()
        try:
            os.system(cmd)
        except:
            print("Alignment failed")


if __name__ == '__main__':

    df = pd.read_csv(parameters.METADA_CSV_PATH)

    df = df[~df.duplicated(['text_path'], keep=False)]
    df = df[~df.duplicated(['audio_path'], keep=False)]

    df['local_audio_path'] = df['audio_path'].apply(lambda x: parameters.AUDIO_FOLDER_PATH + '/' + x.split('/')[-1])
    df['local_text_path'] = df['text_path'].apply(lambda x: parameters.TXT_FOLDER_PATH + '/' + x.split('/')[-1])
    df['local_text_path'] = df['local_text_path'].apply(lambda x: x.replace('.pdf', '.txt'))

    empty_txts = []

    for idx in tqdm(range(len(df))):
        if os.path.isfile(df.iloc[idx]['local_text_path']):

            if os.stat(df.iloc[idx]['local_text_path']).st_size == 0:
                print(df.iloc[idx]['local_text_path'])
                empty_txts.append(df.iloc[idx]['local_text_path'])
                continue
            #print(df.iloc[idx]['local_text_path'])
            ForcedAlignment(df.iloc[idx]['local_audio_path'],
            df.iloc[idx]['local_text_path']).align_audio_and_text(parameters.SYNCMAP_PATH + '/' + df.iloc[idx]['local_audio_path'].split('/')[-1].replace('.mp3', '.json'))
        else:
            print("Text does not exist")

    with open('empty_txt.txt', 'w+') as f:
        for item in empty_txts:
            f.write("%s\n" % item)






