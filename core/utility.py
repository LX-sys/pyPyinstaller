# -*- coding:utf-8 -*-
# @time:2022/11/417:07
# @author:LX
# @file:utility.py
# @software:PyCharm


import sys
import os
import platform

# 根路径
RootPath = os.getcwd()

Windows = "windows"
Linux = "linux"
Mac = "darwin"

# 操作系统
__system= platform.system().lower()

is_system_win = __system == Windows

is_system_linux = __system == Linux

is_system_mac = __system == Mac

# 对同一系统的不同风格的路径进行统一
def path_to_unified(path:str):
    if is_system_win:
        if r"\\" in path:
            return path.replace(r"\\","\\")
    return path


# 修正路径,并返回
def correctionPath(path:str)->str:
    if is_system_mac:
        if "\\" in path:
            return path.replace("\\","/")

    if is_system_win:
        if "/" in path:
            return path.replace("/","\\")

    return path

def Path(*args):
    return os.path.join(RootPath,*args)