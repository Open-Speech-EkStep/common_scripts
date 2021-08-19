# Modified from indic-nlp-library

import sys, codecs, string, itertools, re
from indicnlp import langinfo


class NormalizerI(object):
    """
    The normalizer classes do the following: 
    * Some characters have multiple Unicode codepoints. The normalizer chooses a single standard representation
    * Some control characters are deleted
    * While typing using the Latin keyboard, certain typical mistakes occur which are corrected by the module
    Base class for normalizer. Performs some common normalization, which includes: 
    * Byte order mark, word joiner, etc. removal 
    * ZERO_WIDTH_NON_JOINER and ZERO_WIDTH_JOINER removal 
    * ZERO_WIDTH_SPACE and NO_BREAK_SPACE replaced by spaces 
    Script specific normalizers should derive from this class and override the normalize() method. 
    They can call the super class 'normalize() method to avail of the common normalization 
    """

    BYTE_ORDER_MARK='\uFEFF'
    BYTE_ORDER_MARK_2='\uFFFE'
    WORD_JOINER='\u2060'
    SOFT_HYPHEN='\u00AD'

    ZERO_WIDTH_SPACE='\u200B'
    NO_BREAK_SPACE='\u00A0'

    ZERO_WIDTH_NON_JOINER='\u200C'
    ZERO_WIDTH_JOINER='\u200D'

    def _normalize_punctuations(self, text):
        """
        Normalize punctuations. 
        Applied many of the punctuation normalizations that are part of MosesNormalizer 
        from sacremoses
        """
        text=text.replace(NormalizerI.BYTE_ORDER_MARK,'')
        text=text.replace('„', r'"')
        text=text.replace('“', r'"')
        text=text.replace('”', r'"')
        text=text.replace('–', r'-')
        text=text.replace('—', r' - ')
        text=text.replace('´', r"'")
        text=text.replace('‘', r"'")
        text=text.replace('‚', r"'")
        text=text.replace('’', r"'")
        text=text.replace("''", r'"')
        text=text.replace('´´', r'"')
        text=text.replace('…', r'...')
        return text

    def normalize(self,text):
        pass 

class UrduNormalizer(NormalizerI):
    '''Uses UrduHack library.
    https://docs.urduhack.com/en/stable/_modules/urduhack/normalization/character.html#normalize
    '''

    def __init__(self, lang, remove_nuktas=True):
        self.lang = lang
        self.remove_nuktas = remove_nuktas
    
        from urduhack.normalization import (
            remove_diacritics,
            normalize_characters,
            normalize_combine_characters
        ) # TODO: Use only required normalizers
        from urduhack.preprocessing import (
            normalize_whitespace,
            digits_space,
            all_punctuations_space,
            english_characters_space
        )
        self.normalize_whitespace = normalize_whitespace
        self.digits_space = digits_space
        self.all_punctuations_space = all_punctuations_space
        self.english_characters_space = english_characters_space

        self.remove_diacritics = remove_diacritics
        self.normalize_characters = normalize_characters
        self.normalize_combine_characters = normalize_combine_characters

    def normalize(self, text):
        text=text.replace(NormalizerI.BYTE_ORDER_MARK,'')
        text=text.replace(NormalizerI.BYTE_ORDER_MARK_2,'')
        text=text.replace(NormalizerI.WORD_JOINER,'')
        text=text.replace(NormalizerI.SOFT_HYPHEN,'')

        text=text.replace(NormalizerI.ZERO_WIDTH_SPACE,' ') # ??
        text=text.replace(NormalizerI.NO_BREAK_SPACE,' ')

        text=text.replace(NormalizerI.ZERO_WIDTH_NON_JOINER, '')
        text=text.replace(NormalizerI.ZERO_WIDTH_JOINER,'')
        
        text = self._normalize_punctuations(text)
        text = self.normalize_whitespace(text)
        if self.remove_nuktas:
            text = self.remove_diacritics(text)
        text = self.normalize_characters(text)
        text = self.normalize_combine_characters(text)
        text = self.digits_space(text)
        text = self.all_punctuations_space(text)
        text = self.english_characters_space(text)
        return text