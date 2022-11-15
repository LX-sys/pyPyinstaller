# -*- coding:utf-8 -*-
# @time:2022/11/1015:22
# @author:LX
# @file:fwin.py
# @software:PyCharm


'''
    多页面分离
'''

import os
import sys
import copy
import shutil
import subprocess
from PyQt5.QtCore import QPropertyAnimation, QPoint,pyqtSignal,Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QListWidget,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
    QRadioButton,
    QListWidgetItem,
    QStackedWidget,
    QTextBrowser,
    QFileDialog,
    QMessageBox,
    QProgressBar
)
from libGui.tree import Tree
from core.utility import is_system_win,is_system_mac,correctionPath,path_to_unified
from core.pageThread import PageThread


# 首页(1)
class FirstWin(QWidget):
    oked = pyqtSignal(dict)

    def __init__(self,*args,**kwargs):
        super(FirstWin, self).__init__(*args,**kwargs)
        self.setObjectName("first_win")
        self.setStyleSheet('''
*{
background-color: rgb(38, 82, 120);
}
#first_win{
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
#listWidget_recently,#initial_options{
background-color: rgb(28, 59, 86);
border:1px solid rgb(30, 41, 51);
border-radius:3px;
color:rgb(230, 221, 197);
font: 12pt "等线";
}
#initial_options QAbstractItemView{
background-color: rgb(28, 59, 86);
color:rgb(230, 221, 197);
}    ''')
        self.firstPage()

        self.info = {
            "op":0
        }

    # 首页
    def firstPage(self):
        self.body = QWidget()
        self.body.setFixedSize(670, 520)
        self.body.setObjectName("body")

        # 居中布局
        self.enter_hlag = QHBoxLayout(self)
        self.enter_hlag.addWidget(self.body)

        # 左选项
        self.left_win = QWidget(self.body)
        self.left_win.setFixedSize(280, 450)
        self.left_win.move(200, 30)
        self.left_win.setObjectName("left_win")

        # 初始选项 和按钮
        self.initial_options = QComboBox(self.left_win)
        self.initial_options.setFixedSize(230, 70)
        self.initial_options.move(30, 150)
        self.initial_options.setObjectName("initial_options")
        self.initial_options.addItems(["新项目打包", "最近打包项目"])
        self.ok = QPushButton(self.left_win)
        self.ok.setText("确定")
        self.ok.setFixedSize(230, 70)
        self.ok.move(30, 250)
        self.ok.setObjectName("ok")
        self.initial_options.currentIndexChanged.connect(self.ani_event)  # 动画事件

        # 内部函数
        def op_index(self,index):
            self.info["op"] = index

        self.initial_options.currentIndexChanged.connect(lambda index:op_index(self,index))
        self.ok.clicked.connect(lambda :self.oked.emit(self.info)) # ok事件

        # 最近打包项列表
        self.listWidget_recently = QListWidget(self.body)
        self.listWidget_recently.setFixedSize(280, 450)
        self.listWidget_recently.setObjectName("listWidget_recently")
        self.listWidget_recently.move(370, 30)
        self.listWidget_recently.hide()  # 先隐藏
        self.addRecentlyPro("das")

    # 动画事件
    def ani_event(self, i):
        ani = QPropertyAnimation(self.left_win, b"pos", self)
        ani.setStartValue(self.left_win.pos())
        if i == 1:
            ani.setEndValue(QPoint(30, 30))
            ani.finished.connect(lambda: self.listWidget_recently.show())
        elif i == 0:
            ani.setEndValue(QPoint(200, 30))
            self.listWidget_recently.hide()
        ani.setDuration(600)

        ani.start()

    # 添加最近项目
    def addRecentlyPro(self,text:str):
        self.listWidget_recently.addItem(text)


# 初始配置页(2)
class TwoWin(QWidget):
    beforeed = pyqtSignal()
    submited = pyqtSignal(dict) # 开始配置事件

    def __init__(self,*args,**kwargs):
        super(TwoWin, self).__init__(*args,**kwargs)
        self.setObjectName("first_win")
        self.configurationPage()
        self.info = {
            "scriptType":"普通脚本",
            "editName":"PyCharm",
            "pageWay":"Pyinstaller",
            "sys":"Win"
        }

    def configurationPage(self):
        self.setStyleSheet(r'''
*{
background-color: rgb(38, 82, 120);
}
#logo{
border:1px solid red;
}
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
#win_label{
background-image:url(image/appimage/windows-96-gray.png);
}
#mac_label{
background-image:url(image/appimage/mac-96-gray.png);
}
#win_radio,#mac_radio{
font: 10pt "等线";
color:#fff;
}
#placeholder_win{
border:1px solid yellow;
}
#before_btn{
background-color:gray;
}
#before_btn,#after_btn{
border-radius:5px;
color:#fff;
font: 12pt "等线";
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
#right_win{
background-color:#1c3b56;
}
#project_species{
background-color: rgb(28, 59, 86);
border:1px solid rgb(30, 41, 51);
border-radius:3px;
color:rgb(230, 221, 197);
font: 12pt "等线";
}
        ''')

        # 网格布局
        self.gbox = QGridLayout(self)
        self.logo = QLabel()
        self.logo.setObjectName("logo")
        self.logo.setFixedSize(200, 160)
        self.project_species = QListWidget()  # 项目的种类
        self.project_species.setObjectName("project_species")
        self.project_species.setFixedWidth(200)
        self.right_win = QWidget()  # 右侧主题窗口
        self.right_win.setObjectName("right_win")

        self.gbox.addWidget(self.logo, 0, 0, 1, 1)
        self.gbox.addWidget(self.right_win, 0, 1, 2, 1)
        self.gbox.addWidget(self.project_species, 1, 0, 1, 1)

        self.addProjectSpec("普通脚本")
        self.addProjectSpec("PyQt项目")
        self.addProjectSpec("Web项目")

        # 右侧主题窗口 分为上中下 三部分
        self.right_vbox = QVBoxLayout(self.right_win)  # 垂直布局
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
        self.editor_gbox.setFixedSize(230, 150)
        self.editor_gbox.move(20, 25)

        self.editor_glay = QGridLayout(self.editor_gbox)
        self.editor_glay.setContentsMargins(3, 3, 3, 3)
        self.editor_box = QComboBox()  # 编辑器选择框
        self.editor_box.setObjectName("editor_box")
        self.editor_box.setFixedSize(160, 40)
        self.line_box = QLineEdit()
        self.line_box.setObjectName("line_box")
        self.line_box.setFixedSize(160, 30)
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
        self.editor_box.currentTextChanged.connect(
            lambda ed_name: self.line_box.show() if ed_name == "It" else self.line_box.hide())

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

        self.win_radio.clicked.connect(lambda: self.sys_event(self.win_radio))
        self.mac_radio.clicked.connect(lambda: self.sys_event(self.mac_radio))

        # 中间部分的整体布局
        self.middle_hlay = QHBoxLayout(self.rigth_middle)
        self.page_box = QGroupBox()
        self.page_box.setObjectName("page_box")
        self.page_box.setTitle("打包方式")
        self.page_box.setFixedWidth(280)

        self.p_box_vlay = QVBoxLayout(self.page_box)  # 打包方式里面的垂直布局
        self.p_box_vlay.setContentsMargins(9, 20, 9, 9)
        self.page_way = QComboBox()  # 打包方式
        self.page_way.setObjectName("page_way")
        self.page_way.setFixedHeight(40)
        self.placeholder_win = QWidget()  # 占位,目前还不知道
        self.placeholder_win.setObjectName("placeholder_win")

        self.p_box_vlay.addWidget(self.page_way)
        self.p_box_vlay.addWidget(self.placeholder_win)

        self.addPageWay("Pyinstaller")
        self.addPageWay("Nuitka")

        self.middle_right = QWidget()  # 中间部分的右侧
        self.middle_right.setObjectName("middle_right")

        self.middle_hlay.addWidget(self.page_box)
        self.middle_hlay.addWidget(self.middle_right)

        # 下部分
        self.bottom_hlay = QHBoxLayout(self.rigth_bottom)  # 水平布局
        self.before_btn = QPushButton("返回")
        self.before_btn.setObjectName("before_btn")
        self.before_btn.setFixedSize(55, 55)
        self.after_btn = QPushButton("开始配置打包项目")
        self.after_btn.setObjectName("after_btn")
        self.after_btn.setFixedHeight(55)

        self.bottom_hlay.addWidget(self.before_btn)
        self.bottom_hlay.addWidget(self.after_btn)

        def _ed_box(self,name):
            if name == "It":
                name = self.line_box.text()
                # if not name:
                #     name = "It"
            self.info["editName"]=name

        def _page_way(self,name):
            self.info["pageWay"] = name

        def _pro(self,name):
            self.info["scriptType"]=name

        self.editor_box.currentTextChanged.connect(lambda name:_ed_box(self,name))
        self.page_way.currentTextChanged.connect(lambda name:_page_way(self,name))
        self.project_species.itemClicked.connect(lambda item:_pro(self,item.text()))
        # 返回事件
        self.before_btn.clicked.connect(lambda :self.beforeed.emit())
        self.after_btn.clicked.connect(lambda :self.submited.emit(self.info))

        self.win_radio.setEnabled(False)
        self.mac_radio.setEnabled(False)
        if is_system_win:
            self.win_radio.setChecked(True)
            self.win_label.setStyleSheet('''
            #win_label{
            background-image: url(image/appimage/windows-96-color.png);
            }''')
        if is_system_mac:
            self.mac_radio.setChecked(True)
            self.mac_label.setStyleSheet('''
#mac_label{
background-image:url(image/appimage/mac-96-color.png);
}
            ''')

    def sys_event(self, obj: QRadioButton):
        text = obj.text()
        self.info["sys"] = text
        win_logo = {
            "gray": '''
#win_label{
background-image: url(image/appimage/windows-96-gray.png);
}
''',
            "color": '''
            #win_label{
            background-image: url(image/appimage/windows-96-color.png);
            }'''
        }
        mac_logo = {
            "gray": '''
            #mac_label{
background-image:url(image/appimage/mac-96-gray.png);
}
            ''',
            "color": '''
#mac_label{
background-image:url(image/appimage/mac-96-color.png);
}
'''
        }

        if text == "Win":
            self.win_label.setStyleSheet(win_logo["color"])
            self.mac_label.setStyleSheet(mac_logo["gray"])
        if text == "Mac":
            print("Mac亮图标")
            self.win_label.setStyleSheet(win_logo["gray"])
            self.mac_label.setStyleSheet(mac_logo["color"])

    # 添加项目类型
    def addProjectSpec(self,text:str):
        self.project_species.addItem(text)

    # 添加编辑器名称
    def addEditName(self,name:str):
        self.editor_box.addItem(name)

    # 添加打包方式
    def addPageWay(self,text:str):
        self.page_way.addItem(text)


# 打包程序配置页
class PyPyinstaller(QWidget):
    afed=pyqtSignal()  # 返回事件

    def __init__(self,*args,**kwargs):
        super(PyPyinstaller, self).__init__(*args,**kwargs)

        # 配置檢測
        self.detection_res = None

        # 打包过程线程
        self.page_th = PageThread()

        self.setObjectName("PyPyinstaller")
        self.setStyleSheet('''
*{
color:#fff;
background-color: rgb(5, 32, 56);
}
#st_win{
background-color: rgb(17, 61, 98);
}
#title{
font: italic 20pt "Zapfino";
}
#label_1,#label_2,#label_3,#label_4,#label_5{
background-color: rgb(17, 64, 104);
border-radius:20px;
}

        ''')
        # 上部分布局
        self.py_vlay = QVBoxLayout(self)
        self.head_win = QWidget()
        self.head_win.setObjectName("head_win")
        self.head_win.setFixedHeight(150)
        self.st_win = QStackedWidget()
        self.st_win.setObjectName("st_win")
        self.py_vlay.addWidget(self.head_win)
        self.py_vlay.addWidget(self.st_win)

        # 上部分内部布局
        self.head_vlay = QVBoxLayout(self.head_win)
        self.title = QLabel("Py打包程序")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedHeight(100)
        self.title.setObjectName("title")
        self.progress_win = QWidget()  # 进度条外框
        self.progress_win.setFixedHeight(50)
        self.progress_win.setObjectName("progress_win")
        self.head_vlay.addWidget(self.title)
        self.head_vlay.addWidget(self.progress_win)

        Proogess_Size = (40,40)
        self.progress_win_hlay = QHBoxLayout(self.progress_win)
        self.progress_win_hlay.setContentsMargins(0,0,0,0)
        self.progress_win_hlay.setSpacing(3)
        self.label_1 = QLabel("1")
        self.label_2 = QLabel("2")
        self.label_3 = QLabel("3")
        self.label_4 = QLabel("4")
        self.label_5 = QLabel("5")
        lables = [self.label_1,self.label_2,self.label_3,self.label_4,self.label_5]
        for i,l in enumerate(lables):
            l.setObjectName("label_{}".format(i+1))
            l.setFixedSize(*Proogess_Size)
            l.setAlignment(Qt.AlignCenter)
            self.progress_win_hlay.addWidget(l)
        # ===
        self.win1()
        self.win2()
        self.win3()
        self.win4()

        #===
        self.myEvent()
        # 全局页面索引
        self.PageInfo = 0

        self.st_win.setCurrentIndex(0)
        self.exter_info = dict()

    # 接收来自 初始配置页信息
    def setExternalInfo(self,info):
        self.exter_info = info

    # 配置界面
    def win1(self):
        self.win1 = QWidget()
        self.win1.setObjectName("win1")
        self.win1.setStyleSheet('''
*{
background-color: rgb(17, 61, 98);
color:#fff;
font: 12pt "等线";
}
#pro_entrance_gbox,#pro_info_gbox{
color:#50b1fa;;
}
QGroupBox{
border:3px dashed rgb(51, 109, 158);
border-radius:15px;
}
#pro_show_w{
border:3px dashed rgb(51, 109, 158);
}
#pro_line,#pro_open_btn{
border:1px solid #000;
}
#pro_line{
border-right:none;
}
#pro_open_btn{
border-left:none;
background-color: #000;
}
#pro_open_btn:hover{
background-color: rgb(51, 109, 158);
}
#venv_path{
border:2px solid rgb(30, 41, 51);
border-top:none;
border-left:none;
border-right:none;
}
#app_entrance_label{
color:rgb(255, 62, 23);
}
#app_line{
border:1px solid rgb(85, 170, 255);
border-radius:2px;
}
#op_path_btn,#save_app_dir{
background-color: rgb(51, 109, 158);
border-radius:4px;
}
#op_path_btn:hover,#save_app_dir:hover{
background-color: #28567c;
}
#af_btn,#be_btn{
border-radius:4px;
}
#af_btn{
background-color: gray;
}
#af_btn:hover{
background-color:#555656;
}
#be_btn{
background-color:#3572a3;
}
#be_btn:hover{
background-color:#2c5f86;
}
        ''')
        self.st_win.addWidget(self.win1)

        self.changeBarShow(0)

        self.win_glay = QGridLayout(self.win1)
        self.win_glay.setContentsMargins(3,3,3,3)
        self.win_glay.setSpacing(7)
        self.pro_entrance_gbox = QGroupBox()
        self.pro_entrance_gbox.setObjectName("pro_entrance_gbox")
        self.pro_entrance_gbox.setTitle("项目路径设置")
        self.pro_entrance_gbox.setFixedSize(950,240)

        self.pro_info_gbox = QGroupBox()
        self.pro_info_gbox.setObjectName("pro_info_gbox")
        self.pro_info_gbox.setTitle("项目信息")
        self.pro_info_gbox.setFixedSize(500,340)

        self.pro_show_w = QWidget()
        self.pro_show_w.setObjectName("pro_show_w")
        self.pro_show_w.setFixedSize(440,340)
        self.win_glay.addWidget(self.pro_entrance_gbox,0,0,1,2)
        self.win_glay.addWidget(self.pro_info_gbox,1,0,1,1)
        self.win_glay.addWidget(self.pro_show_w,1,1,1,1)

        # 项目路径内部布局
        self.pro_line = QLineEdit(self.pro_entrance_gbox)
        self.pro_line.setObjectName("pro_line")
        self.pro_line.setFixedSize(660,30)
        self.pro_open_btn = QPushButton("...",self.pro_entrance_gbox)
        self.pro_open_btn.setObjectName("pro_open_btn")
        self.pro_open_btn.setFixedSize(75,30)
        self.pro_line.move(90,30)
        self.pro_open_btn.move(750,30)

        V_Radio = (90,25)
        self.venv_radio = QRadioButton("虚拟环境",self.pro_entrance_gbox)
        self.venv_radio.setObjectName("venv_radio")
        self.venv_radio.setFixedSize(*V_Radio)
        self.v_image = QLabel(self.pro_entrance_gbox)
        self.v_image.setObjectName("v_image")
        self.v_image.setFixedSize(55,55)
        self.local_radio = QRadioButton("本地环境",self.pro_entrance_gbox)
        self.local_radio.setObjectName("local_radio")
        self.local_radio.setFixedSize(*V_Radio)
        self.venv_path = QLineEdit(self.pro_entrance_gbox)
        self.venv_path.setObjectName("venv_path")
        self.venv_path.setFixedSize(730,30)
        self.venv_radio.move(90,100)
        self.v_image.move(420,80)
        self.local_radio.move(730,100)
        self.venv_path.move(90,170)

        # 项目信息部分
        self.app_name = QLabel("可执行程序名称",self.pro_info_gbox)
        self.app_name.setObjectName("app_name")
        self.app_name.setFixedSize(120,30)
        self.app_line = QLineEdit(self.pro_info_gbox)
        self.app_line.setText("main")  # 默认main
        self.app_line.setObjectName("app_line")
        self.app_line.setFixedSize(220,30)
        self.app_name.move(20,40)
        self.app_line.move(150,40)
        self.terminal_comboBox = QComboBox(self.pro_info_gbox)
        self.terminal_comboBox.setObjectName("terminal_comboBox")
        self.terminal_comboBox.addItems(["带终端窗口","不带终端窗口"])
        self.terminal_comboBox.setFixedSize(130,30)
        self.app_comboBox = QComboBox(self.pro_info_gbox)
        self.app_comboBox.setObjectName("terminal_comboBox")
        self.app_comboBox.addItems(["打包成单一程序","包含文件夹"])
        self.app_comboBox.setFixedSize(140,30)
        self.terminal_comboBox.move(20,95)
        self.app_comboBox.move(240,95)
        self.app_entrance_label = QLabel("程序入口文件路径(这个路径直接决定你的程序是否能正常运行)*",self.pro_info_gbox)
        self.app_entrance_label.setObjectName("app_entrance_label")
        self.app_entrance_label.setFixedSize(460,20)
        self.app_entrance_label.move(20,150)
        self.op_path_btn = QPushButton("选择路径",self.pro_info_gbox)
        self.op_path_btn.setObjectName("op_path_btn")
        self.op_path_btn.setFixedSize(80,40)
        self.op_path_btn.move(20,180)
        self.show_op_path = QTextBrowser(self.pro_info_gbox)
        self.show_op_path.setObjectName("show_op_path")
        self.show_op_path.setFixedSize(460,90)
        self.show_op_path.move(20,230)

        # self.pro_show_w上面的布局
        self.af_btn = QPushButton("返回",self.pro_show_w)
        self.af_btn.setObjectName("af_btn")
        self.af_btn.setFixedSize(65,50)
        self.be_btn = QPushButton("下一步",self.pro_show_w)
        self.be_btn.setObjectName("be_btn")
        self.be_btn.setFixedSize(350,50)
        self.af_btn.move(10,280)
        self.be_btn.move(80,280)

        # 项目打包位置
        self.save_app_dir = QPushButton("打包位置",self.pro_show_w)
        self.save_app_dir.setObjectName("save_app_dir")
        self.save_app_dir.setFixedSize(130,40)
        self.save_app_dir.move(20,25)

        self.save_app_dir_show = QTextBrowser(self.pro_show_w)
        self.save_app_dir_show.setObjectName("save_app_dir_show")
        self.save_app_dir_show.setFixedSize(400,100)
        self.save_app_dir_show.move(20,80)

        self.save_app_dir.clicked.connect(lambda :self.page_app_dir_event())

        self.af_btn.clicked.connect(lambda :self.afed.emit())

        # --

    # 检测界面
    def win2(self):
        self.win2 = QWidget()
        self.win2.setObjectName("win2")
        self.st_win.addWidget(self.win2)
        self.win2.setStyleSheet('''
*{
background-color: rgb(17, 61, 98);
color:#fff;
font: 12pt "等线";
}
#btn_detection{
border:1px solid rgb(255, 223, 118);
border-radius:6px;
background-color: rgba(255, 223, 118, 200);
font-size:16pt;
}
#btn_detection:hover{
border-width:2px;
}
#af_btn_1,#be_btn_1{
border-radius:4px;
}
#af_btn_1{
background-color: gray;
}
#af_btn_1:hover{
background-color:#555656;
}
#be_btn_1{
background-color:#3572a3;
}
#be_btn_1:hover{
background-color:#2c5f86;
}
#textBrowser_out{
background-color: rgb(30, 41, 51);
color:#11a611;
}
''')

        self.win2_vlay = QVBoxLayout(self.win2)
        self.win2_vlay.setContentsMargins(0,0,0,0)
        self.win2_vlay.setSpacing(0)
        self.win2_top = QWidget()
        self.win2_buttom = QWidget()
        self.win2_top.setObjectName("win2_top")
        self.win2_buttom.setObjectName("win2_buttom")
        self.win2_top.setFixedHeight(90)
        self.win2_vlay.addWidget(self.win2_top)
        self.win2_vlay.addWidget(self.win2_buttom)

        # win2_top 内部
        self.btn_detection = QPushButton("检测",self.win2_top)
        self.btn_detection.setObjectName("btn_detection")
        self.btn_detection.setFixedSize(110,50)
        self.btn_detection.move(20,25)

        self.af_btn_1 = QPushButton("返回",self.win2_top)
        self.be_btn_1 = QPushButton("下一步",self.win2_top)
        self.af_btn_1.setObjectName("af_btn_1")
        self.be_btn_1.setObjectName("be_btn_1")
        self.af_btn_1.setFixedSize(100,45)
        self.be_btn_1.setFixedSize(110,45)
        self.af_btn_1.move(700,25)
        self.be_btn_1.move(820,25)

        # win2_buttom 内部
        self.win2_b_vlay = QVBoxLayout(self.win2_buttom)
        self.win2_b_vlay.setContentsMargins(3,3,3,3)
        self.textBrowser_out = QTextBrowser()
        self.textBrowser_out.setObjectName("textBrowser_out")
        self.win2_b_vlay.addWidget(self.textBrowser_out)

    # 选择打包资源界面
    def win3(self):
        self.win3 = QWidget()
        self.win3.setObjectName("win3")
        self.st_win.addWidget(self.win3)
        self.win3.setStyleSheet('''
#tree{
border:none;
color:rgb(255, 213, 79);
font: 13pt "等线";
}
#tree::branch:closed:has-children:has-siblings,#tree::branch:open:has-children:!has-siblings {
image:url(image/appimage/tree-chevron-right-16.png);
}
#tree::branch:closed:has-children:!has-siblings,#tree::branch:open:has-children:!has-siblings{
image:url(image/appimage/tree-chevron-down-16.png);
}
#trw_top,#trw_bottom{
border-left:1px solid rgb(66, 129, 178);
}
#af_btn_2,#be_btn_2{
border-radius:4px;
}
#af_btn_2{
background-color: gray;
}
#af_btn_2:hover{
background-color:#555656;
}
#be_btn_2{
background-color:#3572a3;
}
#be_btn_2:hover{
background-color:#2c5f86;
}
        ''')

        #
        self.win3_hlay = QHBoxLayout(self.win3)
        self.win3_hlay.setContentsMargins(0,0,0,0)
        self.win3_hlay.setSpacing(0)
        self.tree = Tree()
        self.tree.header().hide()
        self.tree.setObjectName("tree")
        self.tree.setFixedWidth(500)

        self.tree_right_w = QWidget()
        self.tree_right_w.setObjectName("tree_right_w")

        self.win3_hlay.addWidget(self.tree)
        self.win3_hlay.addWidget(self.tree_right_w)

        # tree_right_w 上下两部分
        self.trw_vlay = QVBoxLayout(self.tree_right_w)
        self.trw_vlay.setContentsMargins(0,0,0,0)
        self.trw_vlay.setSpacing(0)
        self.trw_top = QWidget()
        self.trw_bottom = QWidget()
        self.trw_top.setObjectName("trw_top")
        self.trw_bottom.setObjectName("trw_bottom")
        self.trw_bottom.setFixedHeight(60)
        self.trw_vlay.addWidget(self.trw_top)
        self.trw_vlay.addWidget(self.trw_bottom)

        # trw_bottom内部布局
        self.trw_bottom_hlay = QHBoxLayout(self.trw_bottom)
        self.af_btn_2 = QPushButton("返回")
        self.be_btn_2 = QPushButton("下一步")
        self.af_btn_2.setObjectName("af_btn_2")
        self.be_btn_2.setObjectName("be_btn_2")
        self.af_btn_2.setFixedSize(60,45)
        self.be_btn_2.setFixedHeight(45)
        self.trw_bottom_hlay.addWidget(self.af_btn_2)
        self.trw_bottom_hlay.addWidget(self.be_btn_2)

    # 打包
    def win4(self):
        self.win4 = QWidget()
        self.win4.setObjectName("win4")
        self.st_win.addWidget(self.win4)
        self.win4.setStyleSheet('''
/*#win4_top,#win4_bottom{
border:1px solid red;
}*/
#pbar,#textbro_out{
border:none;
}
#pbar::chunk{
background-color: #11a611;
}
#pbar{
color:#11a611;
}
#textbro_out{
border-top:1px solid #11a611;
}
#page_btn{
border:2px solid rgb(232, 232, 232);
background-color: rgb(161, 161, 161);
color: rgb(0, 0, 0);
border-radius:5px;
font: 16pt "等线";
}
#page_btn:hover{
border-width:1px;
}
#af_btn_3,#be_btn_3{
border-radius:4px;
}
#af_btn_3{
background-color: gray;
}
#af_btn_3:hover{
background-color:#555656;
}
#be_btn_3{
background-color:#3572a3;
}
#be_btn_3:hover{
background-color:#2c5f86;
}
        ''')
        #
        self.win4_vlay = QVBoxLayout(self.win4)
        self.win4_vlay.setSpacing(0)
        self.win4_top = QWidget()
        self.win4_top.setObjectName("win4_top")
        self.win4_top.setFixedHeight(140)
        self.win4_bottom = QWidget()
        self.win4_bottom.setObjectName("win4_bottom")
        self.win4_vlay.addWidget(self.win4_top)
        self.win4_vlay.addWidget(self.win4_bottom)

        # win4_top
        self.page_btn = QPushButton("打包",self.win4_top)
        self.page_btn.setObjectName("page_btn")
        self.page_btn.setFixedSize(160,50)
        self.page_btn.move(20,30)
        self.af_btn_3 = QPushButton("返回",self.win4_top)
        self.be_btn_3 = QPushButton("下一步",self.win4_top)
        self.af_btn_3.setObjectName("af_btn_3")
        self.be_btn_3.setObjectName("be_btn_3")
        self.af_btn_3.setFixedSize(80,45)
        self.be_btn_3.setFixedSize(150,45)
        self.af_btn_3.move(620,30)
        self.be_btn_3.move(730,30)

        # win4_bottom内部
        self.w4_bottom_vlay = QVBoxLayout(self.win4_bottom)
        self.w4_bottom_vlay.setContentsMargins(0,0,0,0)
        self.w4_bottom_vlay.setSpacing(0)
        self.pbar = QProgressBar()
        self.pbar.setObjectName("pbar")
        self.pbar.setFixedHeight(12)
        self.pbar.setMaximum(100)
        self.pbar.setValue(0)
        self.pbar.setTextVisible(False) # 隐藏进度文字
        self.textbro_out = QTextBrowser()
        self.textbro_out.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # 隐藏垂直进度条
        self.textbro_out.setObjectName("textbro_out")
        self.w4_bottom_vlay.addWidget(self.pbar)
        self.w4_bottom_vlay.addWidget(self.textbro_out)

    # 切换进度展示
    def changeBarShow(self,index=0):
        lables = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5]
        for i,l in enumerate(lables):
            if i == index:
                l.setStyleSheet("background-color: rgb(30, 189, 98);")
            else:
                l.setStyleSheet("background-color: rgb(17, 64, 104);")

    # 输出到检测界面
    def outDetection(self,text):
        self.textBrowser_out.append(text)

    # 项目路径事件
    def open_proPath_event(self):
        directory_path = QFileDialog.getExistingDirectory(self, caption="项目目录")
        if directory_path:
            self.textBrowser_out.clear()
            self.btn_detection.setText("检测")
            self.btn_detection.setStyleSheet("background-color: rgba(255, 223, 118, 200);")

            directory_path = correctionPath(directory_path)  # 修正路径
            self.pro_line.setText(directory_path)

            if is_system_win:
                interpreter_path = os.path.join(directory_path, "venv", "Scripts", "python.exe")
            if is_system_mac:
                interpreter_path = os.path.join(directory_path, "venv", "bin", "python")

            interpreter_path = correctionPath(interpreter_path)
            # print("-->",interpreter_path)
            if os.path.isfile(interpreter_path):
                self.venv_radio.setChecked(True)
                interpreter_path = correctionPath(interpreter_path)
                self.venv_path.setText(interpreter_path)
                self.v_image.setStyleSheet('''
                #v_image{
background-image:url(image/appimage/python-venv-55.png);
}
                ''')
            else:
                self.venv_path.clear()
                self.local_radio.setChecked(True)
                self.venv_path.setPlaceholderText("没有找到虚拟环境")
                self.v_image.setStyleSheet('''
                #v_image{
background-image:url(image/appimage/python-local-55.png);
}
                ''')

    # 检查路径的正确性
    def path_detection(self,text,is_mode="dir",f_callback=None,s_callback=None):
        '''

        :param text: 内容
        :param is_mode:
        :param f_callback: 失败调用的回调函数
        :param s_callback: 成功调用的回调函数
        :return:
        '''
        if is_mode == "dir":
            res = os.path.isdir(text)
        if is_mode == "file":
            res = os.path.isfile(text)
        if res:
            if s_callback:
                s_callback()
        else:
            if f_callback:
                f_callback()

    # 虚拟和本地单选按钮切换事件
    def vl_radio_change_event(self,obj:QRadioButton):
        text = obj.text()
        if text == "虚拟环境":
            self.v_image.setStyleSheet("background-image:url(image/appimage/python-venv-55.png);")
        if text == "本地环境":
            self.v_image.setStyleSheet("background-image:url(image/appimage/python-local-55.png);")

    # 选择程序入口文件
    def choose_entrance_file_event(self):
        path = QFileDialog.getOpenFileName(self, caption="选择程序入口文件")
        if path:
            path = correctionPath(path[0])  # 修正
            self.show_op_path.setText(path)

    # 翻页事件
    def turn_page_event(self,direction:str="next"):
        Flag = True # 标记是否翻页

        if self.PageInfo == 0 and direction == "next":
            if not self.venv_path.text() or \
                    not self.pro_line.text() or \
                    not self.show_op_path.toPlainText() or \
                    not self.save_app_dir_show.toPlainText():
                QMessageBox.critical(None, "错误", "信息不完整")
                return

        if self.PageInfo == 1:
            if direction == "top":
                self.tree.clear() # 清空项目树
                self.textBrowser_out.clear()
                self.btn_detection.setText("检测")
                self.btn_detection.setStyleSheet("background-color: rgba(255, 223, 118, 200);")
            if direction == "next":
                if self.btn_detection.text() == "检测":
                    QMessageBox.critical(None,"检测","请先检测")
                    return
                if not self.detection_res:
                    QMessageBox.critical(None, "警告", "检测未通過")
                    return

                # 通过,创建项目数
                self.tree.openTree(self.pro_line.text())

        if self.PageInfo == 2:
            if direction == "top":
                yes = QMessageBox.question(None,"确定?","返回是否清除已选项",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
                if yes == QMessageBox.Yes:
                    self.tree.clear()

            if direction == "next":
                # 重置打包按钮
                self.page_btn.setText("打包")
                self.textbro_out.clear()

                if not self.tree.getStateFiles():
                    QMessageBox.critical(None, "错误", "没有选择任何打包项")
                    return
            # 成功
            print(self.tree.getStateFiles())

        if self.PageInfo == 3:
            if direction == "top":
                yes = QMessageBox.question(None,"确定?","返回是否清除已选项",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
                if yes == QMessageBox.Yes:
                    self.tree.clear()
                    # 由于返回会清除,所以需要再次创建
                    self.tree.openTree(self.pro_line.text())

            if direction == "next":
                pass

        if Flag and direction == "top":
            self.PageInfo -= 1

        if Flag and direction == "next":
            self.PageInfo += 1

        if Flag:
            self.changeBarShow(self.PageInfo)
            self.st_win.setCurrentIndex(self.PageInfo)

    # 配置检测
    def detection_event(self):
        print(self.exter_info)
        self.textBrowser_out.clear()
        self.outDetection("检测中...")
        self.btn_detection.setEnabled(False) # 检测中按钮不可用
        self.detection_res = None  # 重置檢查結果

        # 检测项目目录
        pro_line_text = self.pro_line.text()
        if os.path.isdir(pro_line_text):
            self.outDetection("项目目录: {}".format(pro_line_text))
        else:
            # self.outDetection("项目目录: {}".format(pro_line_text))
            self.outDetection("项目目录: {}".format("找不到项目"))
            self.detection_res = False

        # 检测程序入口文件
        entrance_text = self.show_op_path.toPlainText()
        if os.path.isfile(entrance_text):
            self.outDetection("程序入口文件路径:{}".format(entrance_text))
        else:
            self.outDetection("程序入口文件路径:不存在")
            self.detection_res = False

        # 检测虚拟环境
        venv_path = self.venv_path.text() # 虚拟环境路径
        ra_text = "虚拟环境" if self.venv_radio.isChecked() else "本地环境"
        if os.path.isfile(venv_path):
            self.outDetection("{}: {}".format(ra_text,venv_path))
        else:
            self.outDetection("{}: 不存在".format(ra_text))
            self.detection_res = False

        # 检测python 版本
        try:
            if is_system_win:
                cmd = "{} -V".format(venv_path)
            if is_system_mac:
                cmd ="'{}' -V".format(venv_path)
            po = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            python_v = po.communicate()[0].decode("utf-8")
            if is_system_win:
                python_v = python_v.replace("\r\n","")
            if is_system_mac:
                python_v = python_v.replace("\n", "")
            self.outDetection("{}python版本: {}".format(ra_text,python_v))
        except Exception as e:
            print(e)
            self.outDetection("{}python版本: 没找到python".format(ra_text))
            self.detection_res = False

        # 打包方式
        pageWay = self.exter_info["pageWay"]
        self.outDetection("打包方式:{}".format(pageWay))

        if pageWay == "Pyinstaller":
            pageWay = "pyinstaller"
        if pageWay == "Nuitka":
            pageWay = "Nuitka"

        # 检测pyinstaller/Nuitka有没有安装
        try:
            if is_system_win:
                cmd = "{} -m pip list".format(self.venv_path.text())
            if is_system_mac:
                cmd ="'{}' -m pip list".format(self.venv_path.text())

            pyin = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            piplist = pyin.communicate()[0].decode("utf-8")
            if is_system_win:
                piplist = piplist.split("\r\n")
            if is_system_mac:
                piplist = piplist.split("\n")
            is_pyinstaller = False
            for module_name in piplist[3:]:
                if pageWay in module_name:
                    self.outDetection("{}是否安装: 已安装".format(pageWay))
                    is_pyinstaller = True
                    break
            if is_pyinstaller is False:
                self.outDetection("{}是否安装: 没有安装,请安装 pip install {}".format(pageWay,pageWay))
                self.detection_res = False
        except:
            self.outDetection("{}是否安装: 没有找到python".format(pageWay))
            self.detection_res = False

        # 检测gcc(这个仅对Nuitka有效)
        if pageWay == "Nuitka":
            cmd = "gcc --version"
            try:
                gcc_v = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
                version = gcc_v.stdout.read().decode("utf8")
            except Exception as e:
                version = ""
                self.detection_res = False

            if is_system_mac:
                if "version" in version:
                    self.outDetection("GCC是否安装:{}".format("已安装"))
                else:
                    self.outDetection("GCC是否安装(Nuitka的依赖):{}".format("没有安装gcc"))
                    self.detection_res = False

            if is_system_win:
                if "COLLECT_GCC" in version:
                    self.outDetection("GCC是否安装:{}".format("已安装"))
                else:
                    self.outDetection("GCC是否安装(Nuitka的依赖):{}".format("没有安装gcc,请先下载MinGW64"))
                    self.detection_res = False

        # 终端窗口
        terminal_i = self.terminal_comboBox.currentIndex()
        self.outDetection("是否需要终端窗口: {}".format("需要" if terminal_i==0 else "不需要"))

        # 打包生成方法
        app_i = self.app_comboBox.currentIndex()
        self.outDetection("打包生成方法: {}".format("生成单一程序" if app_i==0 else "包含其他文件"))

        # 打包程序名称
        self.outDetection("可执行程序名称: {}".format(self.app_line.text()))

        # 显示外部信息
        self.outDetection("打包程序类型:{}".format(self.exter_info["scriptType"]))
        self.outDetection("编辑器名称:{}".format(self.exter_info["editName"]))
        self.outDetection("当前操作系统:{}".format(self.exter_info["sys"]))

        # =====
        self.btn_detection.setEnabled(True)  # 解放按钮
        if self.detection_res is None:
            self.detection_res = True
            self.btn_detection.setText("检测通过")
            self.btn_detection.setStyleSheet("background-color: rgb(0, 170, 0);")
        else:
            self.btn_detection.setText("检测失败")
            self.btn_detection.setStyleSheet("background-color: red;")

    # 打包
    def page_event(self):
        r_path = os.path.dirname(self.pro_line.text())
        py_file = self.tree.getStateFiles()

        for i in range(len(py_file)):
            py_file[i]=path_to_unified(os.path.join(r_path,py_file[i]))

        self.pbar.setValue(0) # 重置进度条

        # 寻找入口程序并调整顺序
        entrance_app_path = self.show_op_path.toPlainText()
        if entrance_app_path not in py_file:
            QMessageBox.critical(None,"错误","没有找到入口程序")
            return
        else:
            # 判断位置是否在 0
            index = py_file.index(entrance_app_path)
            if index != 0:
                temp_path = py_file.pop(index)
                py_file.insert(0, temp_path)

            # venv_path =
            # 生成命令
            if is_system_win:
                cmd = "{} -m PyInstaller ".format(self.venv_path.text())

            if is_system_mac:
                cmd = "'{}' -m PyInstaller ".format(self.venv_path.text())

            if self.terminal_comboBox.currentIndex() == 0: # 带终端窗口
                cmd+="-D "
            if self.app_comboBox.currentIndex() ==0: # 打包成单一程序
                cmd+="-F "

            # 程序名称
            cmd += "-n {} ".format(self.app_line.text())

            # 程序文件
            head_file = py_file.pop(0)
            if head_file:
                if is_system_win:
                    cmd += "{} -p ".format(head_file)
                if is_system_mac:
                    cmd += "'{}' -p ".format(head_file)
            else:
                if is_system_win:
                    cmd += "{}".format(head_file)
                if is_system_mac:
                    cmd += "'{}'".format(head_file)

            for path in py_file:
                if is_system_win:
                    cmd+="{};".format(path)
                if is_system_mac:
                    cmd += "'{}';".format(path)
            # print(cmd)

            # 指定输出目录
            save_out_dir = self.save_app_dir_show.toPlainText()

            # 项目名称
            project_name = os.path.basename(self.pro_line.text())
            prodir = path_to_unified(os.path.join(save_out_dir, project_name))
            if not os.path.isdir(prodir):
                os.mkdir(prodir)
                self.save_app_dir_show.setText(prodir)
            save_out_dir = prodir
            print("创建目录:", save_out_dir)

            if save_out_dir:
                if is_system_win:
                    cmd += " --distpath {0} --specpath {0} --workpath {0}".format(save_out_dir)
                # if is_system_mac:
                #     cmd += " --distpath \'{0}\' --specpath \'{0}\' --workpath \'{0}\'".format(save_out_dir)
            print(cmd)
            # 管道执行
            sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            self.page_th.setArgs(sub,self.pbar,self.page_btn)
            self.page_th.start()

    # 打包位置
    def page_app_dir_event(self):
        dir_path = QFileDialog.getExistingDirectory(self, caption="保存目录")
        if dir_path:
            dir_path = correctionPath(dir_path)  # 修正路径
            self.save_app_dir_show.setText(dir_path)

    # 打包过程中的输出信息事件
    def page_info_event(self,info:dict):
        line = info["line"]
        bar = info["bar"]
        # 输出
        self.textbro_out.append(line)
        self.pbar.setValue(bar)

    # 打包完成后的事件
    def page_finish_event(self):
        save_path = self.save_app_dir_show.toPlainText()
        if not save_path:
            return

        print("打包完成后触发")
        r_path = os.path.dirname(self.pro_line.text())

        # 1. 获取资源列表
        resourcefiles = self.tree.getImgResourceFiles()

        for i in range(len(resourcefiles)):
            resourcefiles[i]=path_to_unified(os.path.join(r_path,resourcefiles[i]))

        for old_path in resourcefiles:
            end_name = os.path.basename(old_path)
            new_path = path_to_unified(os.path.join(save_path, end_name))
            if os.path.isdir(old_path) and not os.path.isdir(new_path):
                shutil.copytree(old_path,new_path)
            else:
                shutil.copyfile(old_path,new_path)

        if is_system_mac:
            shutil.move("dist",save_path)
            shutil.move("build",save_path)


        print("资源拷贝完成")

        # 保存的最近项目
        '''
            项目类型
            编辑器
            打包方式
        '''
        # edit_name = self.editor_box


    def myEvent(self):
        # 项目路径事件
        self.pro_open_btn.clicked.connect(self.open_proPath_event)

        # 选择程序入口文件
        self.op_path_btn.clicked.connect(self.choose_entrance_file_event)

        # 路径检查事件
        self.pro_line.textChanged.connect(lambda text:self.path_detection(text,"dir",
                                                                          f_callback=lambda :self.pro_line.setStyleSheet('''border:1px solid red;'''),
                                                                          s_callback=lambda :self.pro_line.setStyleSheet('''border:1px solid #000;''')))
        self.venv_path.textChanged.connect(lambda text:self.path_detection(text,"file",
                                                                           f_callback=lambda :self.venv_path.setStyleSheet('''border-color:red;'''),
                                                                           s_callback=lambda :self.venv_path.setStyleSheet('''border-color:rgb(30, 41, 51);''')))

        self.venv_radio.clicked.connect(lambda :self.vl_radio_change_event(self.venv_radio))
        self.local_radio.clicked.connect(lambda :self.vl_radio_change_event(self.local_radio))

        # 配置检测事件
        self.btn_detection.clicked.connect(self.detection_event)

        # 打包事件
        self.page_btn.clicked.connect(self.page_event)

        # 打包过程线程事件
        self.page_th.sendPageInfo.connect(self.page_info_event)
        self.page_th.finished.connect(self.page_finish_event)

        # win1 下一步事件 -0
        self.be_btn.clicked.connect(lambda :self.turn_page_event(direction="next"))
        # win2 返回事件 -1
        self.af_btn_1.clicked.connect(lambda :self.turn_page_event(direction="top"))
        self.be_btn_1.clicked.connect(lambda :self.turn_page_event(direction="next"))
        # win3 事件 -2
        self.af_btn_2.clicked.connect(lambda :self.turn_page_event(direction="top"))
        self.be_btn_2.clicked.connect(lambda :self.turn_page_event(direction="next"))
        # win4 事件 -3
        self.af_btn_3.clicked.connect(lambda :self.turn_page_event(direction="top"))
        self.be_btn_3.clicked.connect(lambda :self.turn_page_event(direction="next"))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = PyPyinstaller()
    win.show()

    sys.exit(app.exec_())