# -*- coding:utf-8 -*-
# @time:2022/11/4 17:13
# @author:LX
# @file:projectPath.py
# @software:PyCharm


# 项目路径,已经路径下的文件分析
import os,sys
import copy


class ProjectPath:
    PyCharm = "PyCharm"

    def __init__(self):
        self.pro_path = ""
        self.compiler_name = ""

    # 设置项目的路径,入口程序文件名
    def setProjectPath(self,path:str,compiler:str="PyCharm"):
        '''

        :param path: 目录路径
        :param main_file: 入口程序文件名
        :param compiler: 使用的编译器名称
        :return:
        '''
        self.pro_path = path
        self.compiler_name = compiler
        if compiler == ProjectPath.PyCharm:
            self.filter__file = [".idea","__pycache__","venv",".DS_Store",".git"]

    # 生成树
    def tree(self,path,tree_dict:dict):
        '''

        :param path:项目路径
        :param tree_dict: 一个空字典,存储数的结构
        :return:
        '''
        # print(path)
        name = os.path.basename(path)
        tree_dict[name] =[]
        root = os.listdir(path)
        for f in root:
            if f in self.filter__file:
                continue
            join_path = os.path.join(path,f)

            # 文件
            if os.path.isfile(join_path):
                tree_dict[name].append(f)
                # print(join_path)
            elif os.path.isdir(join_path):
                temp={f:[]}
                tree_dict[name].append(temp)
                self.tree(join_path,temp)

if __name__ == '__main__':
    pro = ProjectPath()
    # print(os.listdir(r"/Applications/Python 3.8/save/pyPyinstaller"))
    pro.setProjectPath(r"/Applications/Python 3.8/save/pyPyinstaller",pro.PyCharm)
    t=dict()
    pro.tree(pro.pro_path,t)
    print(t)


