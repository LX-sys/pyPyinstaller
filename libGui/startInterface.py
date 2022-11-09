

import sys
from PyQt5.QtCore import QPropertyAnimation, QPoint
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QStackedWidget,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QGridLayout
)


# 启动界面
class StartInterface(QStackedWidget):
    def __init__(self,*args,**kwargs):
        super(StartInterface, self).__init__(*args,**kwargs)
        self.resize(1000, 800)
        self.setStyleSheet('''
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
        ''')

        # 创建两个窗口
        self.first_win = QWidget()
        self.first_win.setObjectName("first_win")
        self.two_win = QWidget()
        self.two_win.setObjectName("two_win")

        self.addWidget(self.first_win)
        self.addWidget(self.two_win)

        self.firstPage()
        self.configurationPage()

        self.myevent()

    # 首页
    def firstPage(self):
        self.body = QWidget()
        self.body.setFixedSize(670,520)
        self.body.setObjectName("body")

        # 居中布局
        self.enter_hlag = QHBoxLayout(self.first_win)
        self.enter_hlag.addWidget(self.body)

        # 左选项
        self.left_win = QWidget(self.body)
        self.left_win.setFixedSize(280,450)
        self.left_win.move(200,30)
        self.left_win.setObjectName("left_win")

        # 初始选项 和按钮
        self.initial_options =  QComboBox(self.left_win)
        self.initial_options.setFixedSize(230,70)
        self.initial_options.move(30,150)
        self.initial_options.setObjectName("initial_options")
        self.initial_options.addItems(["新项目打包","最近打包项目"])
        self.ok = QPushButton(self.left_win)
        self.ok.setText("确定")
        self.ok.setFixedSize(230,70)
        self.ok.move(30,250)
        self.ok.setObjectName("ok")
        self.initial_options.currentIndexChanged.connect(self.ani_event) # 动画事件

        # 最近打包项列表
        self.listWidget_recently = QListWidget(self.body)
        self.listWidget_recently.setFixedSize(280,450)
        self.listWidget_recently.setObjectName("listWidget_recently")
        self.listWidget_recently.move(370,30)
        self.listWidget_recently.hide() # 先隐藏
        self.addRecentlyPro("das")

    # 配置页面(二)
    def configurationPage(self):
        self.two_win.setStyleSheet('''
        #logo{
        border:1px solid red;
        }
        #right_win{
        border:1px solid red;
        }
        ''')

        # 网格布局
        self.gbox = QGridLayout(self.two_win)
        self.logo = QLabel()
        self.logo.setObjectName("logo")
        self.logo.setFixedSize(200,160)
        self.project_species = QListWidget()  # 项目的种类
        self.project_species.setObjectName("project_species")
        self.project_species.setFixedWidth(200)
        self.right_win = QWidget()
        self.right_win.setObjectName("right_win")

        self.gbox.addWidget(self.logo,0,0,1,1)
        self.gbox.addWidget(self.right_win,0,1,2,1)
        self.gbox.addWidget(self.project_species,1,0,1,1)

        self.addProjctSpec("普通脚本")
        self.addProjctSpec("PyQt项目")
        self.addProjctSpec("Web项目")

    # 动画事件
    def ani_event(self,i):
        print(i)
        ani = QPropertyAnimation(self.left_win,b"pos",self)
        ani.setStartValue(self.left_win.pos())
        if i == 1:
            ani.setEndValue(QPoint(30, 30))
            ani.finished.connect(lambda: self.listWidget_recently.show())
        elif i == 0:
            ani.setEndValue(QPoint(200, 30))
            self.listWidget_recently.hide()
        ani.setDuration(600)

        ani.start()

    # OK按钮的事件
    def ok_event(self):
        index = self.initial_options.currentIndex()
        if index == 0:
            print("进入配置页面")
            self.setCurrentIndex(1)

    # 事件
    def myevent(self):
        self.ok.clicked.connect(self.ok_event)

    # 添加最近项目
    def addRecentlyPro(self,text:str):
        self.listWidget_recently.addItem(text)

    # 添加项目类型
    def addProjctSpec(self,text:str):
        self.project_species.addItem(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = StartInterface()
    win.show()

    sys.exit(app.exec_())