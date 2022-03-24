import pysrt
from perplexity_score_generator import Perplexity
import conf

class MixedSubtitles:
    def __init__(self):
        self.eng_srt = pysrt.open(conf.english_subtitle)
        self.hindi_srt = pysrt.open(conf.hindi_subtitle)

    def chunk_selector(self):
        hindi_perplexity = Perplexity(conf.hindi_lm).subtitle_perplexity(conf.hindi_subtitle)
        for i in range(0, len(self.eng_srt)):
            if len(" ".join(self.eng_srt[i].text.split()).strip().split(" ")) <= len(" ".join(self.hindi_srt[i].text.split()).strip().split(" ")):
                self.eng_srt[i].text = " ".join(self.hindi_srt[i].text.split())
            else:
                self.eng_srt[i].text = " ".join(self.eng_srt[i].text.split())

            if hindi_perplexity[i] <= 1000 and len(" ".join(self.hindi_srt[i].text.split()).strip().split(" ")) > 3:
                self.eng_srt[i].text = " ".join(self.hindi_srt[i].text.split())

        self.eng_srt.save('merged_en_hi_new.srt', encoding='utf-8')


if __name__=='__main__':
    MixedSubtitles().chunk_selector()