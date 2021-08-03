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


if __name__ == '__main__':
    text = ExtractText('/home/anirudh/Desktop/news_on_air_website_data_Text_Regional_Maithili_writereaddata_Bulletins_Text_Regional_2018_Dec_Regional-Patna-Maithily-1815-1820-20181210193927.pdf').get_text()
    print(len(text))
    print(text)
    print(KrutidevToUnicode.convert_to_unicode(';gk\u00a1 is vkidk ;wfudksM'))
