import parameters
from aeneas.exacttiming import TimeValue
from aeneas.executetask import ExecuteTask
from aeneas.language import Language
from aeneas.syncmap import SyncMapFormat
from aeneas.task import Task
from aeneas.task import TaskConfiguration
from aeneas.textfile import TextFileFormat
import aeneas.globalconstants as gc


class ForcedAlignment:
    def __init__(self):
        self.audio_file_path = parameters.AUDIO_FILE_PATH
        self.txt_file_path = parameters.TXT_FILE_PATH

    def align_audio_and_text(self):
        config = TaskConfiguration()
        config[gc.PPN_TASK_LANGUAGE] = Language.HIN
        config[gc.PPN_TASK_IS_TEXT_FILE_FORMAT] = TextFileFormat.PLAIN
        config[gc.PPN_TASK_OS_FILE_FORMAT] = SyncMapFormat.JSON
        task = Task()
        task.configuration = config

        task.audio_file_path_absolute = self.audio_file_path
        task.text_file_path_absolute = self.txt_file_path
        task.sync_map_file_path_absolute = 'data/test.json'
        ExecuteTask(task).execute()
        task.output_sync_map_file()


if __name__ == '__main__':
    ForcedAlignment().align_audio_and_text()




