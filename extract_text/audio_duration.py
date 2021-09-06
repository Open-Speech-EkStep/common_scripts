import sox
from joblib import Parallel,delayed
from tqdm import tqdm
from glob import glob
import parameters


def duration(wav):
    return sox.file_info.duration(wav)


audio_files = glob(parameters.LABELLED_DATA_PATH + '/**/*.wav')
durations = Parallel(n_jobs=-1)(delayed(duration)(wav) for wav in tqdm(audio_files))

print(sum(durations)/3600)
