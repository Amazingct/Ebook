import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import PyPDF2

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head',
	'input',
	'script',
    '✗'
	# there may be more elements you don't want, such as "style", etc.
]
def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

out = epub2text('books/sample.epub')




class Book:
    def __init__(self, bk):

        if bk.endswith("epub"):
            print("EPUB file detected")
            self.author = ''
            self.title = epub.read_epub(bk).title
            self.pages = epub.read_epub(bk).pages
            out = epub2text(bk)
            final = []
            for text in out:
                gan = text.split("\n")
                for g in gan:
                    final.append(g)
            self.text = final


        if bk.endswith("pdf"):
            print("PDF file detected")
            book = open(bk, 'rb')
            pdfReader = PyPDF2.PdfFileReader(book)
            self. pages = pdfReader.numPages
            final = []
            for num in range(0, self.pages):
                page = pdfReader.getPage(num)
                text = page.extractText()
                final.append(text)
            self.text = final
