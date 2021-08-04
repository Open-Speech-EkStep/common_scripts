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
from krutidev_to_unicode import KrutidevToUnicode
import parameters


class ExtractText:
    def __init__(self):
        self.file_path = parameters.PDF_FILE_PATH

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

    def convert_to_unicode(self, sep='।'):
        krutidev_lines = self.get_text().split('\n')
        unicode_lines = [KrutidevToUnicode.convert_to_unicode(line) for line in krutidev_lines]
        combined_text = ''
        for line in unicode_lines:
            words = line.split()
            if len(words) < 5:
                continue
            combined_text = combined_text + ' '.join(words)
        unicode_sentences = combined_text.split(sep=sep)
        return unicode_sentences

    def clean_text(self):
        unicode_sentence_list = self.convert_to_unicode()
        unicode_sentence_list = [l.replace('(', ' ') for l in unicode_sentence_list]
        unicode_sentence_list = [l.replace(')', ' ') for l in unicode_sentence_list]
        unicode_sentence_list = [l.replace('-', '') for l in unicode_sentence_list]
        unicode_sentence_list = [l.replace(',', '') for l in unicode_sentence_list]
        clean_unicode_sentence_list = [l.strip() for l in unicode_sentence_list]
        return clean_unicode_sentence_list

    def create_txt_file(self):
        unicode_sentences_list = self.clean_text()
        txt_file_path = '/'.join(self.file_path.split('/')[:-1])
        txt_file_name = self.file_path.split('/')[-1].replace('.pdf', '.txt')
        with open(os.path.join(txt_file_path, txt_file_name), 'w') as f:
            f.write('\n'.join(unicode_sentences_list))


if __name__ == '__main__':
    text = ExtractText().convert_to_unicode()
    ExtractText().create_txt_file()

