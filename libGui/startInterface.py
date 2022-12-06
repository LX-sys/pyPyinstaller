
import os
import sys
from PyQt5.QtCore import QPropertyAnimation, QPoint
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QStackedWidget,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QGridLayout,
    QGroupBox,
    QLineEdit,
    QRadioButton
)
from core.utility import is_system_win,is_system_mac,save,load
from libGui.st.fwin import FirstWin,TwoWin
from libGui.st.fwin import PyPyinstaller


RECENTLY_FILE = "recently.json"

# 启动界面
class StartInterface(QStackedWidget):
    def __init__(self,*args,**kwargs):
        super(StartInterface, self).__init__(*args,**kwargs)
        self.setObjectName("StartInterface")
        self.resize(1000, 800)
        self.setStyleSheet('''
#StartInterface{
background-color: rgb(5, 32, 56);
}
''')

        self.recently_info=dict()

        # 创建两个窗口
        self.first_win = FirstWin()  #
        self.two_win = TwoWin()
        self.pypyinstaller = PyPyinstaller()
        self.addWidget(self.first_win)
        self.addWidget(self.two_win)
        self.addWidget(self.pypyinstaller)

        self.myevent()

        self.setCurrentIndex(0)

        # 创建最近项目信息
        if not os.path.isfile(RECENTLY_FILE):
            save(RECENTLY_FILE,self.recently_info)
        else:
            # 加载信息
            self.recently_info = load(RECENTLY_FILE)
            for name in self.recently_info.keys():
                self.first_win.addRecentlyPro(name)

    # 选择最近事件
    def recently_event(self,name:str):
        self.pypyinstaller.setRecentlyInfo(self.recently_info[name])
        self.setCurrentIndex(1)

    # 打包完成后,触发保存信息
    def save_recently_event(self,info:dict):
        pro_name = info["pro_name"]
        self.recently_info[pro_name] = info
        save(RECENTLY_FILE, self.recently_info)

    # OK按钮的事件
    def ok_event(self,info:dict):
        index = info["op"]
        if index == 0:
            pass
            print("进入配置页面")

        if index == 1:
            pass
        self.setCurrentIndex(1)

    #
    def two_config_event(self,info:dict):
        self.setCurrentIndex(2)
        # print(info)
        self.pypyinstaller.setExternalInfo(info)

    # 事件
    def myevent(self):
        # 切换页面事件
        self.first_win.oked.connect(self.ok_event)
        self.two_win.beforeed.connect(lambda :self.setCurrentIndex(0))

        # 配置页面提交事件
        self.two_win.submited.connect(self.two_config_event)

        # 返回
        self.pypyinstaller.afed.connect(lambda :self.setCurrentIndex(1))

        # 选择最近事件
        self.first_win.sendTexted.connect(self.recently_event)


        # 打包完成后,触发保存信息
        self.pypyinstaller.pageEnded.connect(self.save_recently_event)
