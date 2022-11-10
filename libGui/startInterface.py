

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
#right_win{
background-color:#1c3b56;
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

        self.setCurrentIndex(0)

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
        self.two_win.setStyleSheet(r'''
        #logo{
        border:1px solid red;
        }
        /*#rigth_top,#rigth_bottom{
        border:1px solid yellow;
        }*/
        

#editor_gbox,#sys_gbox,#page_box,#middle_right{
color: #408bc8;
border:2px solid #3573a7;
font: 12pt "等线";
border-radius:5px;
}
#editor_box,#line_box,#page_way{
background-color: rgb(28, 59, 86);
font: 12pt "等线";
color:#fff;
}
#line_box{
border:1px solid #357dbd;
}
#editor_box QAbstractItemView,#page_way QAbstractItemView{
color:#fff;
background: transparent;
}
/*#win_label,#mac_label{
border:1px solid yellow;
}*/
#win_label{
background-image:url(../image/appimage/windows-96-gray.png);
}
#mac_label{
background-image:url(../image/appimage/mac-96-gray.png);
}
#win_radio,#mac_radio{
font: 10pt "等线";
color:#fff;
}
#placeholder_win{
border:1px solid yellow;
}
#before_btn,#after_btn{
border-radius:5px;
color:#fff;
font: 12pt "等线";
}
#before_btn{
background-color:gray;
}
#before_btn:hover{
background-color:#555656;
}
#after_btn{
background-color:#3572a3;
}
#after_btn:hover{
color:#cecece;
background-color:#2c5f86;
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
        self.right_win = QWidget()  # 右侧主题窗口
        self.right_win.setObjectName("right_win")

        self.gbox.addWidget(self.logo,0,0,1,1)
        self.gbox.addWidget(self.right_win,0,1,2,1)
        self.gbox.addWidget(self.project_species,1,0,1,1)

        self.addProjectSpec("普通脚本")
        self.addProjectSpec("PyQt项目")
        self.addProjectSpec("Web项目")

        # 右侧主题窗口 分为上中下 三部分
        self.right_vbox = QVBoxLayout(self.right_win) # 垂直布局
        self.rigth_top = QWidget()
        self.rigth_middle = QWidget()
        self.rigth_bottom = QWidget()
        self.rigth_top.setObjectName("rigth_top")
        self.rigth_middle.setObjectName("rigth_middle")
        self.rigth_bottom.setObjectName("rigth_bottom")
        self.rigth_top.setFixedHeight(230)
        self.rigth_bottom.setFixedHeight(100)
        self.right_vbox.addWidget(self.rigth_top)
        self.right_vbox.addWidget(self.rigth_middle)
        self.right_vbox.addWidget(self.rigth_bottom)

        # 上部分
        # 代码编辑器
        self.editor_gbox = QGroupBox(self.rigth_top)
        self.editor_gbox.setTitle("代码编辑器")
        self.editor_gbox.setObjectName("editor_gbox")
        self.editor_gbox.setFixedSize(230,150)
        self.editor_gbox.move(20,25)

        self.editor_glay = QGridLayout(self.editor_gbox)
        self.editor_glay.setContentsMargins(3,3,3,3)
        self.editor_box = QComboBox() # 编辑器选择框
        self.editor_box.setObjectName("editor_box")
        self.editor_box.setFixedSize(160,40)
        self.line_box = QLineEdit()
        self.line_box.setObjectName("line_box")
        self.line_box.setFixedSize(160,30)
        self.line_box.setPlaceholderText("输入编辑器名称")
        self.editor_glay.addWidget(self.editor_box)
        self.editor_glay.addWidget(self.line_box)
        self.addEditName("PyCharm")
        self.addEditName("Vscode")
        self.addEditName("Vim")
        self.addEditName("It")
        # 先隐藏,选择其他时显示
        self.line_box.hide()
        # 编辑器选择框事件
        self.editor_box.currentTextChanged.connect(lambda ed_name:self.line_box.show() if ed_name == "It" else self.line_box.hide())

        self.sys_gbox = QGroupBox(self.rigth_top)
        self.sys_gbox.setTitle("操作系统")
        self.sys_gbox.setObjectName("sys_gbox")
        self.sys_gbox.setFixedSize(470, 150)
        self.sys_gbox.move(280, 25)

        ImageSize = (96, 96)
        RadioSize = (96, 20)
        self.wm_hlay = QHBoxLayout(self.sys_gbox)
        self.win_hlay = QVBoxLayout()
        self.win_label = QLabel()
        self.win_label.setObjectName("win_label")
        self.win_label.setFixedSize(*ImageSize)
        self.win_radio = QRadioButton("Win")
        self.win_radio.setObjectName("win_radio")
        self.win_radio.setFixedSize(*RadioSize)
        self.win_hlay.addWidget(self.win_label)
        self.win_hlay.addWidget(self.win_radio)

        self.mac_hlay = QVBoxLayout()
        self.mac_label = QLabel()
        self.mac_label.setObjectName("mac_label")
        self.mac_label.setFixedSize(*ImageSize)
        self.mac_radio = QRadioButton("Mac")
        self.mac_radio.setObjectName("mac_radio")
        self.mac_radio.setFixedSize(*RadioSize)
        self.mac_hlay.addWidget(self.mac_label)
        self.mac_hlay.addWidget(self.mac_radio)
        self.wm_hlay.addLayout(self.win_hlay)
        self.wm_hlay.addLayout(self.mac_hlay)

        self.win_radio.clicked.connect(lambda :self.sys_event(self.win_radio))
        self.mac_radio.clicked.connect(lambda :self.sys_event(self.mac_radio))

        # 中间部分的整体布局
        self.middle_hlay = QHBoxLayout(self.rigth_middle)
        self.page_box = QGroupBox()
        self.page_box.setObjectName("page_box")
        self.page_box.setTitle("打包方式")
        self.page_box.setFixedWidth(280)

        self.p_box_vlay = QVBoxLayout(self.page_box) # 打包方式里面的垂直布局
        self.p_box_vlay.setContentsMargins(9,20,9,9)
        self.page_way = QComboBox() # 打包方式
        self.page_way.setObjectName("page_way")
        self.page_way.setFixedHeight(40)
        self.placeholder_win = QWidget() # 占位,目前还不知道
        self.placeholder_win.setObjectName("placeholder_win")
        self.p_box_vlay.addWidget(self.page_way)
        self.p_box_vlay.addWidget(self.placeholder_win)

        self.addPageWay("Pyinstaller")
        self.addPageWay("Nuitka")

        self.middle_right = QWidget() # 中间部分的右侧
        self.middle_right.setObjectName("middle_right")

        self.middle_hlay.addWidget(self.page_box)
        self.middle_hlay.addWidget(self.middle_right)

        # 下部分
        self.bottom_hlay = QHBoxLayout(self.rigth_bottom) # 水平布局
        self.before_btn = QPushButton("返回")
        self.before_btn.setObjectName("before_btn")
        self.before_btn.setFixedSize(55,55)
        self.after_btn = QPushButton("开始配置配置项目")
        self.after_btn.setObjectName("after_btn")
        self.after_btn.setFixedHeight(55)

        self.bottom_hlay.addWidget(self.before_btn)
        self.bottom_hlay.addWidget(self.after_btn)


        # 返回事件
        self.before_btn.clicked.connect(lambda :self.setCurrentIndex(0))

        # 根据当前系统选择
        if is_system_win:
            self.win_radio.setChecked(True)
            self.win_label.setStyleSheet('''
            #win_label{
            background-image: url(../image/appimage/windows-96-color.png);
            }''')
        if is_system_mac:
            self.mac_radio.setChecked(True)
            self.mac_label.setStyleSheet('''
#mac_label{
background-image:url(../image/appimage/mac-96-color.png);
}
''')

    # 动画事件
    def ani_event(self,i):
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

    # 系统选择事件
    def sys_event(self,obj:QRadioButton):
        win_logo = {
            "gray":'''
#win_label{
background-image: url(../image/appimage/windows-96-gray.png);
}
''',
            "color":'''
            #win_label{
            background-image: url(../image/appimage/windows-96-color.png);
            }'''
        }
        mac_logo={
            "gray":'''
            #mac_label{
background-image:url(../image/appimage/mac-96-gray.png);
}
            ''',
            "color":'''
#mac_label{
background-image:url(../image/appimage/mac-96-color.png);
}
'''
        }

        text = obj.text()
        if text == "Win":
            self.win_label.setStyleSheet(win_logo["color"])
            self.mac_label.setStyleSheet(mac_logo["gray"])
        if text == "Mac":
            print("Mac亮图标")
            self.win_label.setStyleSheet(win_logo["gray"])
            self.mac_label.setStyleSheet(mac_logo["color"])


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
    def addProjectSpec(self,text:str):
        self.project_species.addItem(text)

    # 添加编辑器名称
    def addEditName(self,name:str):
        self.editor_box.addItem(name)

    # 添加打包方式
    def addPageWay(self,text:str):
        self.page_way.addItem(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = StartInterface()
    win.show()

    sys.exit(app.exec_())