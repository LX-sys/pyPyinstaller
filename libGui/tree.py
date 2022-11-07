
import sys
import copy
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QTreeWidget,
    QTreeWidgetItem,
)
from core.utility import is_system_win,is_system_mac
from core.projectAnalysis.projectPath import ProjectPath

'''
    Tree带选择框
'''


class Tree(QTreeWidget):
    # 所有选中项字典信号
    treeCheckStateListed = pyqtSignal(list)

    def __init__(self,*args,**kwargs):
        super(Tree, self).__init__(*args,**kwargs)

        # 分隔符

        self.separator = "/"
        if is_system_win:
            self.separator = "\\"

        self.checkState_paths = []

        self.setObjectName("tree")
        self.pro = ProjectPath()
        # self.pro.setProjectPath(r"D:\code\wpTranscribe", pro.PyCharm)
        # t = dict()
        # self.pro.tree(pro.pro_path, t)
        # # print(t)
        # print("==================")
        # self.createTree(t)
        self.openTree(r"D:\code\wpTranscribe")

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
                self.checkState_paths.remove(cur_item_xpath)
        #
        # # 所有路径拼成完整路径
        # for i in range(len(self.checkState_paths)):
        #     if self.checkState_paths[i][0] == self.separator:
        #         self.checkState_paths[i] = cur_item_xpath + self.checkState_paths[i]
        #
        # 最终路径列表
        print(self.checkState_paths)
        # self.treeCheckStateListed.emit(self.checkState_paths)

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
                    # flag = True
                    # for p in self.checkState_paths:  # 判定路径是否存在
                    #     if part_path in p:
                    #         flag = False
                    #         break
                    # if flag:
                    #     self.checkState_paths.append(part_path)
                    cu_item_xpath= self.xpathItem(i)
                    if cu_item_xpath not in self.checkState_paths:
                        self.checkState_paths.append(cu_item_xpath)
                else:
                    self.getStateFile(self.getItem(i),part_path)
        return copy.copy(self.checkState_paths)  # 这里必须返回copy,不能直接返回


    def myEvent(self):
        self.itemClicked.connect(self.checkState_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Tree()
    win.show()

    sys.exit(app.exec_())