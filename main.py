import PyPDF2
from PIL import Image
import pdfreader

with open('rimkevich_10_11_klass.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfFileReader(pdf_file) # extracting images from the 1st page
    # printing first page contents
    pdf_page = pdf_reader.getPage(0)
    print(pdf_page.extractText())

    # reading all the pages content one by one
    for page_num in range(pdf_reader.numPages):
        pdf_page = pdf_reader.getPage(page_num)
        print(pdf_page.extractText())

def parse_text(text):
    result = {}
    pairs = text.split(';')
    for pair in pairs:
        if len(pair.strip()) == 0:
            continue
        parts = pair.split(' is ')
        key = parts[0].strip().lstrip("set '").rstrip("'")
        print(key)
        value = int(parts[1].strip())
        result[key] = value
    return result

print(parse_text("<< set 'aenat' is -4677; set'isgece'is -676; set 'raus'is -1737; set'useded_30' is 3398;>>"))