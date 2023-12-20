# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:09:21 2020

@author: user1
"""
import fitz
import os
folder = r'./pdf_merger_output'
output = os.path.join(folder, 'output.pdf') # 输出文件
filelist = os.listdir(folder) # 获取pdf文件名
doc_merger = fitz.open()
for filename in filelist:
    path = os.path.join(folder, filename) # pdf的绝对路径
    print(path)
    doc = fitz.open(path)
    doc_merger.insertPDF(doc)
doc_merger.save(r'./pdf_merger_output/output.pdf')
    
'''
doc1=fitz.open(r'./1.pdf')
doc2=fitz.open(r'./2.pdf')
doc3=fitz.open(r'./Doc1.pdf')
doc1.insertPDF(doc2)
doc1.insertPDF(doc3)
doc1.save(r'./new1.pdf')
'''
