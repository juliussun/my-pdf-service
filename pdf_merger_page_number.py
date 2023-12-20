import sys
import os
import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfFileWriter, PdfFileReader
def create_pdf_with_pagenumber(tmp, num):
    '''create tmp pdf that only include page number'''
    pdfmetrics.registerFont(
        TTFont('Times-New-Roman', 'C:\\Windows\\Fonts\\times.ttf'))
    c = canvas.Canvas(tmp)
    for i in range(num):
        c.setFont('Times-New-Roman', 10)
        c.drawString((104)*mm, (4)*mm, str(i + 1))
        c.showPage()
    c.save()
def main():
    path = './pdf_merger_output/output.pdf'
    if len(sys.argv) == 1:
        if not os.path.isfile(path):
            sys.exit(1)
    else:
        path = os.path.basename(sys.argv[1])
    tmp = "./pdf_merger_output/tmp.pdf"
    dst_pdf = PdfFileWriter()
    with open(path, 'rb') as f:
        src_pdf = PdfFileReader(f, strict=False)
        n = src_pdf.getNumPages()
        create_pdf_with_pagenumber(tmp, n)
        with open(tmp, 'rb') as ftmp:
            num_pdf = PdfFileReader(ftmp)
            for i in range(n):
                print('page: %d of %d' % (i+1, n))
                page = src_pdf.getPage(i)
                num_layer = num_pdf.getPage(i)
                page.mergePage(num_layer)
                dst_pdf.addPage(page)
        if dst_pdf.getNumPages():
            output = '.{}_withpagenumber.pdf'.format(path.split('.')[1])
            with open(output, 'wb') as f:
                dst_pdf.write(f)
        os.remove(tmp)
if __name__ == "__main__":
    main()