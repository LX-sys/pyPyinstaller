# -*- coding:utf-8 -*-
# @time:2022/11/513:47
# @author:LX
# @file:__init__.py.py
# @software:PyCharm

# import os
# import sys
# import subprocess
# s= "'/Applications/Python 3.8/save/pyPyinstaller/venv/bin/python' -V"
# print(s)
# subprocess.Popen(s,stdout=subprocess.PIPE,shell=True)
# print()

import subprocess

# PyInstaller
# f = open(r"D:\code\pyPyinstaller\log.txt","a")
cmd =r"D:\code\excelGenerate\venv\Scripts\python.exe -m PyInstaller -D -F -n main D:\code\excelGenerate\main.py -p D:\code\excelGenerate\operation\down.py;D:\code\excelGenerate\operation\readExcel.py;D:\code\excelGenerate\operation\WriteExcel.py;D:\code\excelGenerate\operation\__init__.py;D:\code\excelGenerate\core\excel.py;D:\code\excelGenerate\core\utility.py;D:\code\excelGenerate\core\__init__.py;"
s=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
while s.poll() is None:
    line =s.stdout.readline()
    line =line.strip()
    if line:
        print("信息:",line)
    # if s.returncode == 0:
    #     print("ss")
# python_v = s.communicate()[0].decode("utf-8")
# print("===")
# print(python_v)
# print("===")
# f.close()