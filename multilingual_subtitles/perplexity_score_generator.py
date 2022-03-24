import pysrt
import kenlm
import conf

class Perplexity:
    def __init__(self, model):
        self.lm = kenlm.Model(model)

    def sentence_perplexity(self, sentence):
        return self.lm.perplexity(sentence)

    def subtitle_perplexity(self, subtitle):
        srt = pysrt.open(subtitle)
        perplexity = []

        for i, _ in enumerate(srt):
            
            perplexity.append(self.sentence_perplexity(srt[i].text))

        return perplexity

    
if __name__ == '__main__':

    p = Perplexity(conf.hindi_lm).subtitle_perplexity(conf.hindi_subtitle)
