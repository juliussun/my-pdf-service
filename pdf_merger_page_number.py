"""
Created on Tue Nov 17 11:09:21 2020

@author: user1

pip install reportlab

output file is named output_withpagenumber
"""

import sys
import os
import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfWriter, PdfReader
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
    dst_pdf = PdfWriter()
    with open(path, 'rb') as f:
        src_pdf = PdfReader(f, strict=False)
        n = len(src_pdf.pages)
        create_pdf_with_pagenumber(tmp, n)
        with open(tmp, 'rb') as ftmp:
            num_pdf = PdfReader(ftmp)
            for i in range(n):
                print('page: %d of %d' % (i+1, n))
                page = src_pdf.pages[i]
                num_layer = num_pdf.pages[i]
                page.merge_page(num_layer)
                dst_pdf.add_page(page)
        if len(dst_pdf.pages):
            output = '.{}_withpagenumber.pdf'.format(path.split('.')[1])
            with open(output, 'wb') as f:
                dst_pdf.write(f)
        os.remove(tmp)
if __name__ == "__main__":
    main()