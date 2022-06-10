from indicnlp.tokenize.indic_tokenize import trivial_tokenize
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

lang = 'hi'
normalizer = IndicNormalizerFactory().get_normalizer(lang)

def normalize_text(sent):
    normalized = normalizer.normalize(sent)
    text = ' '.join(trivial_tokenize(normalized, lang))
    text=text.replace('\u090d','\u090f'+ '\u0901') # Custom rule 1 for ऍ
    return text
