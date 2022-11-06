# -*- coding:utf-8 -*-
# @time:2022/11/5 13:47
# @author:LX
# @file:pyPyinstaller.py
# @software:PyCharm
import os
import sys
import subprocess
# from PyQt5.Qt import Qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
    QGroupBox,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QComboBox,
    QFileDialog,
    QTextBrowser
)
from libGui.tree import Tree
from core.utility import Path,is_system_win,is_system_mac,correctionPath,Mac,Windows

class PyPyinstaller(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(PyPyinstaller, self).__init__(*args,**kwargs)
        self.coreWin = QWidget()
        self.coreWin.setObjectName("coreWin")
        self.setCentralWidget(self.coreWin)
        self.resize(1200,800)

        # ---- 打包信息
        self.page_info = {
            "project_path": "",  # 项目路径
            "environment_name": "虚拟环境",  # 打包环境
            "interpreter_path": "",  # 解释器路径
            "is_win": True,  # 是否带终端窗口
            "is_one_app": True,  # 是否打包成单一程序
            "op_sys": "",  # 选择的操作系统
            "app_name": "main"  # 程序的名称
        }

        # 多窗口
        self.st = QStackedWidget()
        self.st_win_1 = QWidget()
        self.st_win_1.setObjectName("st_win_1")
        self.st_win_2 = QWidget()
        self.st_win_2.setObjectName("st_win_2")
        self.st_win_3 = QWidget()
        self.st_win_3.setObjectName("st_win_3")
        self.st.addWidget(self.st_win_1)
        self.st.addWidget(self.st_win_2)
        self.st.addWidget(self.st_win_3)

        self.initLayout()
        self.setStyleSheet(
'''
#coreWin{
background-color: rgb(0, 0, 0);
/*border:1px solid rgb(255, 255, 255);
color: rgb(255, 255, 255);*/
}
QLabel{
color:#fff;
}
#app_name{
color:#000;
}
#win_top{
border-bottom:1px solid gray;
background-color:#254f72;
}
#title{
font: 30pt "等线";
}
#win_top_left{
/*border:1px solid #ffff7f;*/
background-color:#254f72;
}
#t_v1,#t_v2,#t_v3,#t_v4,#t_v5{
font: 17pt "等线";
}
/*#t_v1:hover,#t_v2:hover,#t_v3:hover,#t_v4:hover,#t_v5:hover{
background-color:#ffdf76;
color:#254f72;
}*/
#st_win_1,#st_win_2,#st_win_3{
background-color:#ffdf76;
}
QGroupBox{
border:1px solid #254f72;
font: 10pt "等线";
}
#open_dir,#venv_path_open_dir,#btn_entrance{
background-color:#ffdf76;
}
QComboBox{
border:1px solid #254f72;
}
QComboBox QAbstractItemView{
color:#254f72;
background: transparent;
}
#next_p_1,#next_p_1,#next_p_2{
border:1px solid #00aa00;
background-color:#00aa00;
color:#fff;
}
#next_p_1:hover,#next_p_1:hover,#next_p_2:hover{
border:1px solid #00aa00;
background-color:#005500;
color:#fff;
}
#detection_btn{
border:none;
background-color:gray;
color:#fff;
font: 20pt "等线";
}
#detection_btn:hover{
background-color:#272727;
}
#textBrowser_checkinfo{
background-color:#000;
color:#fff;
font: 15pt "等线";
}
#label_entrance{
color:red;
}
'''
        )

        self.myEvent()

        self.setTitle("Py项目打包程序")
        self.st.setCurrentIndex(0)
        self.leftStyleTrack(0)

    def setTitle(self,text:str):
        self.title.setText(text)
        self.title.move(self.width() // 2 - self.title.width(), 100 - self.title.height())

    def initLayout(self):
        # 整体的上下布局
        self.win_top = QWidget()
        self.win_buttom = QWidget()
        self.win_top.setObjectName("win_top")
        self.win_buttom.setObjectName("win_buttom")

        self.win_top.setMinimumHeight(200)
        self.win_top.setMaximumHeight(200)

        self.lay_t_b = QVBoxLayout(self.coreWin)
        self.lay_t_b.setContentsMargins(0,0,0,0)
        self.lay_t_b.setSpacing(0)
        self.lay_t_b.addWidget(self.win_top)
        self.lay_t_b.addWidget(self.win_buttom)

        # 上半部分
        self.title = QLabel(self.win_top)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("title")

        # 下半部分布局(self.lay_t_b)
        self.win_top_left = QWidget()
        self.win_top_right = QWidget()
        self.win_top_left.setObjectName("win_top_left")
        self.win_top_right.setObjectName("win_top_right")

        self.win_top_left.setMinimumWidth(240)
        self.win_top_left.setMaximumWidth(240)

        self.lay_t_b_t = QHBoxLayout(self.win_buttom)
        self.lay_t_b_t.setContentsMargins(0,0,0,0)
        self.lay_t_b_t.setSpacing(0)
        self.lay_t_b_t.addWidget(self.win_top_left)
        self.lay_t_b_t.addWidget(self.win_top_right)

        # 下半部分-左侧布局
        self.t_v1 = QLabel()
        self.t_v2 = QLabel()
        self.t_v3 = QLabel()
        self.t_v4 = QLabel()
        self.t_v5 = QLabel()
        self.t_v1.setObjectName("t_v1")
        self.t_v2.setObjectName("t_v2")
        self.t_v3.setObjectName("t_v3")
        self.t_v4.setObjectName("t_v4")
        self.t_v5.setObjectName("t_v5")
        self.t_v1.setAlignment(Qt.AlignCenter)
        self.t_v2.setAlignment(Qt.AlignCenter)
        self.t_v3.setAlignment(Qt.AlignCenter)
        self.t_v4.setAlignment(Qt.AlignCenter)
        self.t_v5.setAlignment(Qt.AlignCenter)
        self.t_v1.setText("1. 预设置")
        self.t_v2.setText("2. 检查")
        self.t_v3.setText("3. 选择打包资源")
        self.t_v4.setText("4. 打包")
        self.t_v5.setText("5. 完成")

        self.lay_tbt_l = QVBoxLayout(self.win_top_left)
        self.lay_tbt_l.setContentsMargins(0,0,0,0)
        self.lay_tbt_l.setSpacing(0)
        self.lay_tbt_l.addWidget(self.t_v1)
        self.lay_tbt_l.addWidget(self.t_v2)
        self.lay_tbt_l.addWidget(self.t_v3)
        self.lay_tbt_l.addWidget(self.t_v4)
        self.lay_tbt_l.addWidget(self.t_v5)

        # 下半部分-右侧布局

        self.lay_tbt_r = QHBoxLayout(self.win_top_right)
        self.lay_tbt_r.setContentsMargins(0,0,0,0)
        self.lay_tbt_r.setSpacing(0)
        self.lay_tbt_r.addWidget(self.st)

        # ---
        self.win1()
        self.win2()
        self.win3()

    # 左侧样式跟随
    def leftStyleTrack(self,i):
        temp =[self.t_v1,self.t_v2,self.t_v3,self.t_v4,self.t_v5]
        temp[i].setStyleSheet('''
background-color:#ffdf76;
color:#254f72;
            ''')
        temp.remove(temp[i])
        for i in temp:
            i.setStyleSheet("")

    # 预设置界面
    def win1(self):
        self.pro_gbox = QGroupBox(self.st_win_1)
        self.pro_gbox.setObjectName("pro_gbox")
        self.pro_gbox.setGeometry(10,20,900,80)
        self.pro_gbox.setTitle("项目路径设置")

        self.pro_path = QLineEdit(self.pro_gbox)
        self.pro_path.setGeometry(10,30,600,30)
        self.open_dir = QPushButton("...",self.pro_gbox)
        self.open_dir.setObjectName("open_dir")
        self.open_dir.setGeometry(610,30,40,30)

        # -------- 打包环境
        self.pro_environment = QGroupBox(self.st_win_1)
        self.pro_environment.setObjectName("pro_environment")
        self.pro_environment.setGeometry(10,120,900,80)
        self.pro_environment.setTitle("打包环境")

        self.ra_venv = QRadioButton("虚拟环境",self.pro_environment)
        self.ra_loac = QRadioButton("本地环境",self.pro_environment)
        self.ra_venv.setGeometry(10,30,121,41)
        self.ra_loac.setGeometry(100,30,121,41)
        self.ra_venv.setChecked(True)  # 默认虚拟环境

        self.venv_path = QLineEdit(self.pro_environment)
        self.venv_path.setGeometry(180,34,450,30)
        self.venv_path_open_dir = QPushButton("...",self.pro_environment)
        self.venv_path_open_dir.setObjectName("venv_path_open_dir")
        self.venv_path_open_dir.setGeometry(630,34,40,30)

        # -----项目信息
        self.pro_info = QGroupBox(self.st_win_1)
        self.pro_info.setTitle("项目信息")
        self.pro_info.setObjectName("pro_info")
        self.pro_info.setGeometry(10,220,500,370)

        self.app_name = QLabel("可执行程序名称",self.pro_info)
        self.app_name.setObjectName("app_name")
        self.app_name.setGeometry(10,30,110,30)
        self.line_app_name = QLineEdit(self.pro_info)
        self.line_app_name.setText("main")
        self.line_app_name.setGeometry(110,30,110,30)

        self.win_bobox = QComboBox(self.pro_info)
        self.win_bobox.setGeometry(10,80,130,25)
        self.win_bobox.addItem("带终端窗口")
        self.win_bobox.addItem("不带终端窗口")

        self.win_program = QComboBox(self.pro_info)
        self.win_program.setGeometry(190,80,130,25)
        self.win_program.addItem("打包成单一程序")
        self.win_program.addItem("包含文件夹")

        self.label_entrance = QLabel("程序入口文件路径(这个路径直接决定你的程序是否能正常运行)*",self.pro_info)
        self.label_entrance.setGeometry(10,120,380,30)
        self.line_entrance = QLineEdit(self.pro_info)
        self.line_entrance.setGeometry(10,160,380,30)
        self.btn_entrance = QPushButton("...",self.pro_info)
        self.btn_entrance.setGeometry(390,160,40,30)
        self.label_entrance.setObjectName("label_entrance")
        self.line_entrance.setObjectName("line_entrance")
        self.btn_entrance.setObjectName("btn_entrance")


        # -------操作系统
        self.sys_box = QGroupBox(self.st_win_1)
        self.sys_box.setTitle("操作系统")
        self.sys_box.setGeometry(530,220,380,120)

        self.ra_win = QRadioButton("Win",self.sys_box)
        self.ra_win.setGeometry(40,50,80,30)
        self.ra_mac = QRadioButton("Mac",self.sys_box)
        self.ra_mac.setGeometry(260,50,80,30)

        self.ra_mac.setEnabled(False)
        self.ra_win.setEnabled(False)

        # 根据系统来决定
        if is_system_win:
            self.ra_win.setChecked(True)
            self.page_info["op_sys"] = Windows
        if is_system_mac:
            self.ra_mac.setChecked(True)
            self.page_info["op_sys"] = Mac

        # ------
        self.next_p_0 = QPushButton("下一步",self.st_win_1)
        self.next_p_0.setObjectName("next_p_1")
        self.next_p_0.setGeometry(800,530,100,30)

    # 检查界面
    def win2(self):
        self.detection_btn = QPushButton("检测",self.st_win_2)
        self.detection_btn.setObjectName("detection_btn")
        self.detection_btn.setGeometry(20,30,164,40)

        # 显示检测信息框
        self.textBrowser_checkinfo = QTextBrowser(self.st_win_2)
        self.textBrowser_checkinfo.setObjectName("textBrowser_checkinfo")
        self.textBrowser_checkinfo.setGeometry(20,90,900,500)

        # 上一步/下一步
        self.up_1 = QPushButton("上一步",self.st_win_2)
        self.next_p_1 = QPushButton("下一步",self.st_win_2)
        self.up_1.setObjectName("up_1")
        self.next_p_1.setObjectName("next_p_1")
        self.up_1.setGeometry(650,30,120,40)
        self.next_p_1.setGeometry(780,30,120,40)

    # 选择打包资源
    def win3(self):
        # 数
        self.tree = Tree()
        self.tree_right = QWidget()
        self.tree_right.setObjectName("tree_right")
        self.tree.setMinimumWidth(500)
        self.tree.setMaximumWidth(500)

        self.tree_box = QHBoxLayout(self.st_win_3)
        self.tree_box.setContentsMargins(0,0,0,0)

        self.tree_box.addWidget(self.tree)
        self.tree_box.addWidget(self.tree_right)

        # 上一步/下一步
        self.up_2 = QPushButton("上一步",self.tree_right)
        self.next_p_2 = QPushButton("下一步",self.tree_right)
        self.up_2.setObjectName("up_2")
        self.next_p_2.setObjectName("next_p_2")

        self.up_2.setGeometry(160,540,120,40)
        self.next_p_2.setGeometry(300,540,120,40)


    # 输出到检测界面
    def outDetection(self,text):
        self.textBrowser_checkinfo.append(text)

    # 下一事件
    def next_event(self,i):
        if i == 1:
            self.page_info["project_path"] = self.pro_path.text() # 项目目录
        self.st.setCurrentIndex(i)
        self.leftStyleTrack(i)

    # 打开项目目录
    def open_pro_dir_event(self):
        directory_path = QFileDialog.getExistingDirectory(self, caption="项目目录")
        directory_path = correctionPath(directory_path) # 修正路径
        self.pro_path.setText(directory_path)
        self.page_info["project_path"]=directory_path

        # 选择目录的同时,简单查找一下解释器路径
        if self.ra_venv.isChecked():
            if is_system_win:
                interpreter_path = os.path.join(directory_path,"venv","Scripts","python.exe")
            elif is_system_mac:
                interpreter_path = os.path.join(directory_path, "venv", "bin", "python")

            interpreter_path = correctionPath(interpreter_path)

            if os.path.isfile(interpreter_path):
                self.venv_path.setText(interpreter_path)
                self.page_info["interpreter_path"]=interpreter_path
                self.venv_path.setEnabled(True)
        print(self.page_info)

    # 选择解释器
    def open_interpreter_event(self):
        path=QFileDialog.getOpenFileName(self,caption="选择解释器")
        if path:
            path = path[0]
            self.venv_path.setText(path)
            self.page_info["interpreter_path"]=path

    # 选择程序入口文件
    def choose_entrance_file_event(self):
        path = QFileDialog.getOpenFileName(self, caption="选择程序入口文件")
        if path:
            path = path[0]
            self.line_entrance.setText(path)

    # 检测事件
    def detection_event(self):
        self.textBrowser_checkinfo.clear() # 清屏
        # 检测项目目录
        if os.path.isdir(self.pro_path.text()):
            self.outDetection("项目目录: {}".format(self.pro_path.text()))
        else:
            self.outDetection("项目目录: {}".format(self.pro_path.text()))

        # 检测程序入口文件
        if os.path.isfile(self.line_entrance.text()):
            self.outDetection("程序入口文件路径:{}".format(self.line_entrance.text()))
        else:
            self.outDetection("程序入口文件路径:不存在")

        # 检测虚拟环境
        venv_path = self.venv_path.text() # 虚拟环境路径
        if os.path.isfile(venv_path):
            self.outDetection("虚拟环境: {}".format(venv_path))
        else:
            self.outDetection("虚拟环境: 不存在")

        # 检测python 版本
        try:
            po = subprocess.Popen("'{}' -V".format(venv_path),
                                  stdout=subprocess.PIPE,
                                  shell=True)
            python_v = po.communicate()[0].decode("utf-8")
            if is_system_win:
                python_v = python_v.replace("\r\n","")
            if is_system_mac:
                python_v = python_v.replace("\n", "")
            self.outDetection("虚拟环境python版本: {}".format(python_v))
        except Exception as e:
            print(e)
            self.outDetection("虚拟环境python版本: 没有python")

        # 检测pyinstaller有没有安装
        try:
            pyin = subprocess.Popen("'{}' -m pip list".format(self.venv_path.text()),
                                    stdout=subprocess.PIPE,
                                    shell=True)
            piplist = pyin.communicate()[0].decode("utf-8")
            if is_system_win:
                piplist = piplist.split("\r\n")
            if is_system_mac:
                piplist = piplist.split("\n")
            is_pyinstaller = False
            for module_name in piplist[3:]:
                if "pyinstaller" in module_name:
                    self.outDetection("pyinstaller是否安装: 已安装")
                    is_pyinstaller = True
                    break
            if is_pyinstaller is False:
                self.outDetection("pyinstaller是否安装: 没有安装,请安装 pip install pyinstaller")
        except:
            self.outDetection("pyinstaller是否安装: 没有找到python")

        # 终端窗口
        self.outDetection("是否需要终端窗口: {}".format("需要" if self.page_info["is_win"] else "不需要"))

        # 打包生成方法
        self.outDetection("打包生成方法: {}".format("生成单一程序" if self.page_info["is_one_app"] else "包含其他文件"))

        # 操作系统
        self.outDetection("操作系统: {}".format(self.page_info["op_sys"]))
        # 打包程序名称
        self.page_info["app_name"] = self.line_app_name.text()
        self.outDetection("可执行程序名称: {}".format(self.page_info["app_name"]))

    # 是否需要终端窗口事件
    def win_bobox_event(self,i):
        if i == 0:
            self.page_info["is_win"] = True
        elif i == 1:
            self.page_info["is_win"] = False

    # 是否需要打包方式事件
    def win_program_event(self,i):
        if i == 0:
            self.page_info["is_one_app"] = True
        elif i == 1:
            self.page_info["is_one_app"] = False


    def myEvent(self):
        self.next_p_0.clicked.connect(lambda :self.next_event(1))

        # 第二页 -- 上一步/下一步
        self.up_1.clicked.connect(lambda :self.next_event(0))
        self.next_p_1.clicked.connect(lambda :self.next_event(2))

        # 打开目录
        self.open_dir.clicked.connect(self.open_pro_dir_event)
        self.venv_path_open_dir.clicked.connect(self.open_interpreter_event)
        self.btn_entrance.clicked.connect(self.choose_entrance_file_event)

        # 第三页 -- 上一步/下一步
        self.up_2.clicked.connect(lambda: self.next_event(1))
        self.next_p_2.clicked.connect(lambda: self.next_event(3))

        # 检测
        self.detection_btn.clicked.connect(self.detection_event)

        # 终端窗口切换事件
        self.win_bobox.currentIndexChanged.connect(self.win_bobox_event)
        # 打包方式切换事件
        self.win_program.currentIndexChanged.connect(self.win_program_event)


    def resizeEvent(self, e: QResizeEvent) -> None:
        # print(e.size().width())
        self.title.move(e.size().width() // 2-50, 100 - self.title.height())
        super(PyPyinstaller, self).resizeEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = PyPyinstaller()
    win.show()

    sys.exit(app.exec_())


