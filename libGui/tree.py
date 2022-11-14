
import sys
import copy
from PyQt5.QtCore import Qt,pyqtSignal,QPoint
from PyQt5.QtGui import QCursor,QColor
from PyQt5.QtWidgets import (
    QApplication,
    QTreeWidget,
    QTreeWidgetItem,
    QMenu
)
from core.utility import is_system_win,is_system_mac
from core.projectAnalysis.projectPath import ProjectPath

'''
    Tree带选择框
'''


class Tree(QTreeWidget):

    def __init__(self,*args,**kwargs):
        super(Tree, self).__init__(*args,**kwargs)

        # 分隔符

        self.separator = "/"
        if is_system_win:
            self.separator = "\\"

        # 选中的路径
        self.checkState_paths = []
        # 标记的资源路径
        self.imgFlag_paths = []

        self.setObjectName("tree")
        self.pro = ProjectPath()
        # self.openTree(r"D:\code\excelGenerate")

        # 注册右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_Event)

        self.myEvent()

    def openTree(self,path:str,compiler:str="PyCharm"):
        self.pro.setProjectPath(path,compiler)
        t = dict()
        self.pro.tree(path, t)
        self.createTree(t)

    # 创建项目目录
    def createTree(self,tree:dict,praret=None):
        for dir in tree:
            # 创建父目录
            r_item = QTreeWidgetItem()
            r_item.setText(0,dir)
            r_item.setCheckState(0,Qt.Unchecked)
            if praret is None:
                self.addTopLevelItem(r_item)
            else:
                praret.addChild(r_item)

            # 创建子目录/文字
            for c_file in tree[dir]:
                if type(c_file) == dict: # 目录
                    self.createTree(c_file,r_item)
                else: # 文件
                    file_item = QTreeWidgetItem()
                    file_item.setText(0,c_file)
                    file_item.setCheckState(0, Qt.Unchecked)
                    r_item.addChild(file_item)

    # 更新树
    def updateTree(self,tree:dict,praret=None):
        # 创建树之前,先清空,避免出现意外
        self.clear()
        self.createTree(tree,praret)

    def clear(self) -> None:
        self.checkState_paths.clear()
        super(Tree, self).clear()

    # 给定一个节点,返回到节点的路径
    def xpathItem(self,item:QTreeWidgetItem)->str:
        # 路径列表
        paths = []
        r_item = item

        while r_item:
            paths.insert(0, r_item.text(0))
            r_item = r_item.parent()

        separator = "{}".format(self.separator)
        return separator.join(paths)

    # 勾选文件事件
    def checkState_event(self,item:QTreeWidgetItem):
        checkState =Qt.Checked if item.checkState(0) else Qt.Unchecked

        items = self.getItem(item)
        cur_item_xpath = self.xpathItem(item)  # 当前点击节点的xpath

        self.allState(items, checkState)
        imperfect_paths = self.getStateFile(items)

        if checkState == Qt.Checked:
            # 单点文件节点,如果是文件则路径完整,不需要拼接
            if "." in cur_item_xpath.split(self.separator)[-1] and cur_item_xpath not in self.checkState_paths:
                self.checkState_paths.append(cur_item_xpath)
        else:# 取消勾选
            cu_text = item.text(0)
            if "." not in cu_text:
                for t in imperfect_paths:
                    if cu_text in t:
                        self.checkState_paths.remove(t)
            else:
                if cur_item_xpath in self.checkState_paths:
                    self.checkState_paths.remove(cur_item_xpath)
        # print(self.checkState_paths)

    # 返回所有选择的文件
    def getStateFiles(self)->list:
        return self.checkState_paths

    # 返回所有资源文件
    def getImgResourceFiles(self)->list:
        return self.imgFlag_paths

    # 返回当前对象下面的项
    def getItem(self,item):
        if type(item) == Tree:
            return [item.topLevelItem(i) for i in range(item.topLevelItemCount())]
        elif item.parent() is None or type(item.parent()) is QTreeWidgetItem:
            return [item.child(i) for i in range(item.childCount())]

    # 返回当前对象下面的项
    def getItemText(self,item):
        return [i.text(0) for i in self.getItem(item)]

    # 选择父目录时,同时选择所有/取消子目录
    def allState(self,item:QTreeWidgetItem=None,checkState=Qt.Checked):
        if item is None:
            root = self.getItem(self)
        else:
            root = item
        for i in root:
            i.setCheckState(0, checkState)
            if "." not in i.text(0):
                self.allState(self.getItem(i), checkState)

    # 标记父目录时,同时标记所有/取消子目录
    def allFlag(self,item:QTreeWidgetItem=None,color=QColor(0,255,0)):
        if item is None:
            root = self.getItem(self)
        else:
            root = item
        for i in root:
            i.setForeground(0,color)
            if "." not in i.text(0):
                self.allFlag(self.getItem(i), color)
            # else:
            #     self.imgFlag_paths.append(self.xpathItem(i))

    # 获取所有勾选的文件
    def getStateFile(self,item:QTreeWidgetItem=None,path=""):
        if item is None:
            root = self.getItem(self)
        else:
            root = item

        for i in root:
            cur_text = i.text(0)  # 当前文件名
            if i.checkState(0):
                part_path = path+self.separator+cur_text  # 部分路径
                if "." in cur_text: # 路径完整
                    cu_item_xpath= self.xpathItem(i)
                    if cu_item_xpath not in self.checkState_paths:
                        self.checkState_paths.append(cu_item_xpath)
                else:
                    self.getStateFile(self.getItem(i),part_path)
        return copy.copy(self.checkState_paths)  # 这里必须返回copy,不能直接返回

    # 右键事件
    def menu_Event(self, pos: QPoint):
        # 当前右键选中的节点
        currentItem = self.itemAt(pos)
        # 创建菜单
        menu = QMenu()
        #
        image_name = menu.addAction("标记为资源文件")
        if currentItem:
            image_name.triggered.connect(lambda :self.img_flag_event(currentItem))

        # 显示菜单
        menu.exec_(QCursor.pos())

    # 标记事件
    def img_flag_event(self,item:QTreeWidgetItem):
        color_v = item.foreground(0).color().name()
        if color_v == "#00ff00":
            item.setForeground(0,QColor(255, 213, 79))
            color = QColor(255, 213, 79)
        elif color_v == "#ffd54f" or color_v == "#000000":
            item.setForeground(0,QColor(0,255,0))
            color = QColor(0,255,0)
            self.imgFlag_paths.append(self.xpathItem(item))

        items = self.getItem(item)
        self.allFlag(items,color)
        if color_v == "#00ff00":
            self.imgFlag_paths.clear()
        print(self.getImgResourceFiles())


    def myEvent(self):
        self.itemClicked.connect(self.checkState_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Tree()
    win.show()

    sys.exit(app.exec_())