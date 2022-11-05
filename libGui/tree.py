
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
)
from core.projectAnalysis.projectPath import ProjectPath



class Tree(QTreeWidget):
    def __init__(self,*args,**kwargs):
        super(Tree, self).__init__(*args,**kwargs)

        pro = ProjectPath()
        pro.setProjectPath(r"/Applications/Python 3.8/save/pyPyinstaller", "main.py", pro.PyCharm)
        t = dict()
        pro.tree(pro.pro_path, t)
        print(t)
        print("==================")
        self.createTree(t)

        self.myEvent()

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

    def checkState_event(self,item:QTreeWidgetItem):
        print(item.text(0),"-->",item.checkState(0))
        print(item.childCount())

    def myEvent(self):
        self.itemClicked.connect(self.checkState_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Tree()
    win.show()

    sys.exit(app.exec_())