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


# 返回当前系统名称
def currentSystemName():
    if is_system_mac:
        return Mac
    if is_system_linux:
        return Linux
    if is_system_win:
        return Windows


print(currentSystemName())

def Path(*args):
    return os.path.join(RootPath,*args)