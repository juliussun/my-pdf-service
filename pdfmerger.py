# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import PyPDF2

folder = r'./pdf_merger_output'
output = os.path.join(folder, 'output.pdf') #输出文件
filelist = os.listdir(folder) # 获取pdf文件名
merger = PyPDF2.PdfFileMerger() 
for filename in filelist:
    path = os.path.join(folder, filename) # pdf的绝对路径
    print(path)
    merger.append(path, bookmark=filename[:-4]) # 合并并贴标签

with open(output, 'wb') as f:
    merger.write(f) # 输出
