# import os
# def create_datatbase(dt_name):
#     #dt_name = input("请输入数据库名字：")
#     path = r'C:\Users\xld\Desktop\1\pythonProject1\data'
#     os.mkdir(path + './dt_name')
#
import os
import shutil
import tkinter.messagebox

import dbf


# 测试用例
# 如果文件夹已经存在，则不能再新创建文件夹，运行时会报错；
# r 声明其后字符串不需要转义，因为 ** \ ** 在被做为转义字符使用；
# 所有关于文件夹的操作文件夹前面要加 ‘./’ 或者 '/' ，如 ‘./file1’ ， ‘/file1’。
def NewDatabase(db_name):
    # 提示用户输入数据库名称，并把变量存储到db_name
    path = os.getcwd()
    os.mkdir(path + r'\\' + db_name)
    os.mkdir(path + r'\\' + db_name + r'\\' + 'SQL')  # 生成的文件夹用来存放sql文件
    # print(path + r'\\' + db_name + r'\\' + 'NONE.dbf')
    # 生成占位文件
    table = dbf.Table(filename=path + r'\\' + db_name + r'\\' + 'NONE.dbf', field_specs='Nothing C(1);',
                      codepage='cp936')
    tkinter.messagebox.showinfo("", "新建数据库" + db_name + '成功!')


def DeleteDatabase(db_name):
    path = os.getcwd()
    shutil.rmtree(path + r'\\' + db_name)
    print("成功删除数据库" + db_name + '!')


if __name__ == '__main__':
    NewDatabase('B')
    # DeleteDatabase('C')
