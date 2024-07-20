# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:09:21 2020

@author: juliussun
"""

import pymupdf
import os
from typing import Optional


def pdf_merger(folder: str, output_folder: Optional[str]) -> dict[str, str]:
    filelist = os.listdir(folder)
    filelist.sort()
    doc_merger = pymupdf.open()

    for filename in filelist:
        file_path = os.path.join(folder, filename)
        print(file_path)
        doc = pymupdf.open(file_path)
        doc_merger.insert_pdf(doc)
        os.unlink(file_path)

    if output_folder is None:
        output_folder = os.path.join(os.path.dirname(folder), "pdf_output")
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

    for existing_output_file in os.listdir(output_folder):
        existing_output_path = os.path.join(output_folder,existing_output_file)
        if os.path.isfile(existing_output_path):
            os.unlink(existing_output_path)
    
    output_path = os.path.join(output_folder, "merged_pdf.pdf")
    doc_merger.save(output_path)
    return {"message": "PDFs merged successfully on backend", "output_path": output_path}
