import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from io import StringIO
# from krutidev_unicode_converter import krutidev_to_unicode
# from Shreedev_Unicode_converter import shreedev_to_unicode
# from gurmukhi_converter import drchaitrik_to_unicode
import parameters
from glob import glob
from tqdm import tqdm
import subprocess
import requests
from joblib import Parallel, delayed

# import nltk
# from nltk.corpus import words

class ExtractText:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_text(self):
        with open(self.file_path, 'rb') as input_file:

            parser = PDFParser(input_file)
            document = PDFDocument(parser)

            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed

            rsrcmgr = PDFResourceManager()
            output_string = StringIO()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
        return output_string.getvalue()

    def txt_from_response(self, line, url='http://localhost:3000/user/'):
        
        PARAMS = {'text': line}
        try:
            req = requests.get(url=url, params=PARAMS)
            data = req.json()
            
            output_text = data['UnicodeText']
            unicode_text = output_text.replace('ଞ୍ଚ', ' ')

        except:
            return 'Bad Character!'

        return unicode_text

    def encoding_to_unicode(self, encoded_text):
        return drchaitrik_to_unicode(encoded_text)

    def filter_english_text(self, encoded_text):
        lines = encoded_text
        
        enc_lines = []
        
        for line in lines:
            line.replace('\n', '\\n')
            print(line)
            words = line.split(' ')

            while("" in words) :
                words.remove("")
            
            false_count = 0
            true_count = 0
            
            for word in words:
                print(word in words.words())
                if word in words.words() == False: 
                    false_count+=1
                elif word in words.words() == True: 
                    true_count+=1
                    print(word)
        
            print('False Count: ', false_count)
            print('True Count: ', true_count)

            if false_count > true_count:
                line = ''
                enc_lines.append(line)
            else:
                enc_lines.append(line)

            while("" in enc_lines) :
                enc_lines.remove("")        
        return enc_lines

    def filter_text(self, encoded_text):
        encoded_text_lines = encoded_text

        enc_lines = []
        encoded_text_lines = [i for i in encoded_text_lines if i and i != ' ']
        
        for line in encoded_text_lines:
            rejection_case = ['@ûeþG^þdê i´f_êeþ', 'RNU', 'Sambalpur', 'SAMBALPURI', 'January', 'February', \
                            'March','April', 'May', 'June', 'July', 'August', 'September', 'October', \
                            'November', 'December', '****************************']
            if any(x in line for x in rejection_case):
                #print(line)
                continue

            enc_lines.append(line)
                
        return enc_lines

    def convert_to_unicode(self, sep=' ।'):
        encoded_lines = self.get_text().split('\n')
        #enc_text = self.filter_english_text(encoded_lines)
        enc_text = self.filter_text(encoded_lines)
        
        unicode_lines = Parallel(n_jobs=-1)(delayed(self.txt_from_response)(line) for line in tqdm(enc_text) if line)
        
        combined_text = ''
        for line in unicode_lines:
            words = line.split()
            if len(words) < 1:
                continue
            combined_text = combined_text + ' '.join(words) + ' '

        unicode_sentences = combined_text.split(sep=sep)
        if len(unicode_sentences) < 3:
            print(unicode_sentences)
        return unicode_sentences

    def clean_text(self):
        unicode_sentence_list = self.convert_to_unicode()
        unicode_sentence_list = [l.replace('(', ' ') for l in unicode_sentence_list]
        unicode_sentence_list = [l.replace(')', ' ') for l in unicode_sentence_list]
        unicode_sentence_list = [l.replace('-', '') for l in unicode_sentence_list]
        unicode_sentence_list = [l.replace(',', '') for l in unicode_sentence_list]
        clean_unicode_sentence_list = [l.strip() for l in unicode_sentence_list]
        #print(clean_unicode_sentence_list)
        #print(len(clean_unicode_sentence_list))
        return clean_unicode_sentence_list

    def create_txt_file(self, file_path):
        unicode_sentences_list = self.clean_text()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unicode_sentences_list))


if __name__ == '__main__':
    pdf_folder_path = parameters.PDF_FOLDER_PATH
    txt_folder_path = parameters.TXT_FOLDER_PATH
    os.makedirs(txt_folder_path, exist_ok=True)
    pdf_files = glob(pdf_folder_path + '/' + '*.pdf')

    for pdf_file in tqdm(pdf_files):
        #print(pdf_file)
        #cmd = "strings " + pdf_file + " | grep FontName"

        try:
            txt_file_name = pdf_file.split('/')[-1].replace('.pdf', '.txt')
            ExtractText(pdf_file).create_txt_file(txt_folder_path + '/' + txt_file_name)

            # text_encodings = subprocess.check_output(cmd, shell=True, text=True, encoding='utf-8')
            # encoding_check = text_encodings.find('Kruti')
            # if encoding_check != -1:
            #     txt_file_name = pdf_file.split('/')[-1].replace('.pdf', '.txt')
            #     ExtractText(pdf_file).create_txt_file(txt_folder_path + '/' + txt_file_name)
            # else:
            #     print('Multiple encodings ', pdf_file)
        except:
            print("Text not extractable ", pdf_file)