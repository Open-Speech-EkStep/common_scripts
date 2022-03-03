import pysrt
import os

def generate_merged_srt():
    for i in range(0, len(en_lm_subs)):
        if len(" ".join(en_lm_subs[i].text.split()).strip().split(" ")) <= len(" ".join(hi_lm_subs[i].text.split()).strip().split(" ")):
            if hi_lm_subs[i].text != '':
                en_lm_subs[i].text = " ".join(hi_lm_subs[i].text.split())
        else:
            en_lm_subs[i].text = " ".join(en_lm_subs[i].text.split())

    en_lm_subs.save('merged_en_hi-0.srt', encoding='utf-8')
    
if __name__ == '__main__':
    en_lm_subs = pysrt.open('subtitles/subtitle_file_eng_lm.srt', encoding='utf-8')
    hi_lm_subs = pysrt.open('subtitles/subtitle_file_hindi_lm.srt', encoding='utf-8')

    if len(en_lm_subs) == len(hi_lm_subs):
        print("Length: ",len(en_lm_subs))
        generate_merged_srt()

    else:
        print("English and Hindi srt file length mismatch!\n")
    
    
    