import pysrt
import kenlm
import matplotlib.pyplot as plt
import sys
import pandas as pd

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

    p = Perplexity(sys.argv[1]).subtitle_perplexity(sys.argv[2])

    df = pd.DataFrame({'perplexity': p})
    df.to_csv(sys.argv[3], index=False)

    
