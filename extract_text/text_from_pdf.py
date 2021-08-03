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


if __name__ == '__main__':
    text = ExtractText('/home/anirudh/Desktop/news_on_air_website_data_Text_Regional_Maithili_writereaddata_Bulletins_Text_Regional_2018_Dec_Regional-Patna-Maithily-1815-1820-20181210193927.pdf').convert_to_unicode()
    #print(len(text))
    #print(text)

