
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QTreeWidgetItemIterator
)
from core.projectAnalysis.projectPath import ProjectPath



class Tree(QTreeWidget):
    def __init__(self,*args,**kwargs):
        super(Tree, self).__init__(*args,**kwargs)

        self.setObjectName("tree")
        pro = ProjectPath()
        pro.setProjectPath(r"/Applications/Python 3.8/save/pyPyinstaller", "main.py", pro.PyCharm)
        t = dict()
        pro.tree(pro.pro_path, t)
        print(t)
        print("==================")
        self.createTree(t)

        self.myEvent()
        # self.getStateFile()

    # 创建项目目录
    def createTree(self,tree:dict,praret=None):
        for dir in tree:
            # 创建父目录
            r_item = QTreeWidgetItem()
            r_item.setText(0,dir)
            r_item.setCheckState(0,False)
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
                    file_item.setCheckState(0, False)
                    r_item.addChild(file_item)

    # 勾选文件事件
    def checkState_event(self,item:QTreeWidgetItem):
        count = item.childCount()
        if item.checkState(0):
            for i in range(count):
                item.child(i).setCheckState(0,Qt.Checked)
        else:
            for i in range(count):
                item.child(i).setCheckState(0, Qt.Unchecked)

    # 获取所有勾选的文件
    def getStateFile(self,count_=None,litem=None):
        print(self.topLevelItemCount())
        print(self.topLevelItem(0).childCount())
        print(self.topLevelItem(0).child(0).child(0).childCount())

        # print(self.selectedItems())
        if count_ is None:
            count = self.topLevelItemCount()
        else:
            count = count_
        for i in range(count):
            if count_ is None:
                self.getStateFile(self.topLevelItem(i).childCount())
            else:
                print("Dsa")


    def myEvent(self):
        self.itemClicked.connect(self.checkState_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Tree()
    win.show()

    sys.exit(app.exec_())