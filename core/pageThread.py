# -*- coding:utf-8 -*-
# @time:2022/11/1217:37
# @author:LX
# @file:pageThread.py
# @software:PyCharm

import time
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QPushButton,QProgressBar


# 打包过程的线程
class PageThread(QThread):
    '''

        发送打包过程中的信息,避免造下面的错误
        QObject::connect: Cannot queue arguments of type 'QTextCursor'
        (Make sure 'QTextCursor' is registered using qRegisterMetaType().)
        这个错误原因是在程序在线程中 QTextBrowser 对这个控件使用append()
    '''
    sendPageInfo = pyqtSignal(dict)
    finished = pyqtSignal(str)  # 打包完成的信号

    def __init__(self,*args,**kwargs):
        super(PageThread, self).__init__(*args,**kwargs)
        self.sub = None  # type:subprocess.Popen
        self.pbar = None  # type:QProgressBar
        self.page_btn = None  # type:QPushButton

    def setArgs(self,sub,pbar,page_btn):
        self.sub = sub
        self.pbar = pbar
        self.page_btn = page_btn

    def run(self) -> None:
        self.page_btn.setText("打包中")
        self.page_btn.setEnabled(False)

        start_time = time.time()
        while self.sub.poll() is None:
            line = self.sub.stdout.readline()
            line = line.strip().decode("utf-8")
            if line:
                self.sendPageInfo.emit({"line":line,"bar":self.pbar.value()+1})

        self.sendPageInfo.emit({"line": "打包完成", "bar": self.pbar.maximum()})
        self.page_btn.setText("完成")
        self.page_btn.setEnabled(True)

        #
        self.finished.emit(str(round(time.time()-start_time,2)))
