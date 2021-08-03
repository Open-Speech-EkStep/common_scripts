from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from io import StringIO


class ExtractText:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_text(self):

        fp = open(self.file_path, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)

        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr = PDFResourceManager()
        output_string = StringIO()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
        print(output_string.getvalue())
        fp.close()


if __name__ == '__main__':
    ExtractText('/home/anirudh/Desktop/news_on_air_website_data_Text_Regional_Maithili_writereaddata_Bulletins_Text_Regional_2018_Dec_Regional-Patna-Maithily-1815-1820-20181210193927.pdf').get_text()
