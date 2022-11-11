

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
from core.utility import is_system_win,is_system_mac
from libGui.st.fwin import FirstWin,TwoWin
from libGui.st.fwin import PyPyinstaller


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

        # 创建两个窗口
        self.first_win = FirstWin()  #
        self.two_win = TwoWin()
        self.pypyinstaller = PyPyinstaller()
        self.addWidget(self.first_win)
        self.addWidget(self.two_win)
        self.addWidget(self.pypyinstaller)

        self.myevent()

        self.setCurrentIndex(0)

    # OK按钮的事件
    def ok_event(self,info:dict):
        print(info)
        index = info["op"]
        if index == 0:
            print("进入配置页面")
            self.setCurrentIndex(1)

    #
    def two_config_event(self,info:dict):
        self.setCurrentIndex(2)
        print(info)

    # 事件
    def myevent(self):
        # 切换页面事件
        self.first_win.oked.connect(self.ok_event)
        self.two_win.beforeed.connect(lambda :self.setCurrentIndex(0))

        # 配置页面提交事件
        self.two_win.submited.connect(self.two_config_event)

        # 返回
        self.pypyinstaller.afed.connect(lambda :self.setCurrentIndex(1))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = StartInterface()
    win.show()

    sys.exit(app.exec_())