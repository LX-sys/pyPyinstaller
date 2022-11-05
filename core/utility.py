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

# 操作系统
__system= platform.system().lower()

is_system_win = __system == "windows"

is_system_linux = __system == "linux"

is_system_mac = __system == "darwin"


def Path(*args):
    return os.path.join(RootPath,*args)