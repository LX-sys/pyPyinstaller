

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

# 启动界面
class StartInterface(QStackedWidget):
    def __init__(self,*args,**kwargs):
        super(StartInterface, self).__init__(*args,**kwargs)
        self.resize(1000, 800)
        self.setStyleSheet('''
*{
background-color: rgb(38, 82, 120);
}
#first_win,#two_win{
background-color: rgb(38, 82, 120);
}   
#body{
border:2px solid rgb(30, 41, 51);
border-radius:10px;
}
#ok{
background-color: rgb(255, 217, 92);
font: 14pt "等线";
border:none;
border-radius:3px;
}
#ok:hover{
background-color: rgb(220, 198, 91);
color: rgb(255, 255, 255);
}
#listWidget_recently,#initial_options,#project_species{
background-color: rgb(28, 59, 86);
border:1px solid rgb(30, 41, 51);
border-radius:3px;
color:rgb(230, 221, 197);
font: 12pt "等线";
}
#initial_options QAbstractItemView{
background-color: rgb(28, 59, 86);
color:rgb(230, 221, 197);
}
#right_win{
background-color:#1c3b56;
}
        ''')

        # 创建两个窗口
        self.first_win = FirstWin()  # 用QLabel播放视频
        self.two_win = TwoWin()
        self.addWidget(self.first_win)
        self.addWidget(self.two_win)


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
        print(info)

    # 事件
    def myevent(self):
        # 切换页面事件
        self.first_win.oked.connect(self.ok_event)
        self.two_win.beforeed.connect(lambda :self.setCurrentIndex(0))

        # 配置页面提交事件
        self.two_win.submited.connect(self.two_config_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = StartInterface()
    win.show()

    sys.exit(app.exec_())