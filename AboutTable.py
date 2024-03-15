import dbf
import os
import tkinter

from ReadWrite import rd


# 创建表 by 薛李丹
def CreateTable(file, struct, path):  # 这里path是相对路径
    # 创建表的.dbf文件
    filename = path + '\\' + file + '.dbf'
    structfile = path + '\\' + file + '_struct.dbf'
    # print(filename)
    # print(structfile)
    # 创建结构文档
    table = dbf.Table(filename=structfile, field_specs='name C(25);type C(25);notNull C(5);isKey C(5)',
                      codepage='cp936')
    # 修改为读写模式
    table.open(mode=dbf.READ_WRITE)
    for i in struct:
        table.append(tuple(i))
    length = len(table)
    table.close()
    # 创建数据文档，要预留槽位
    new_field = ''
    for Mess in struct:
        new_field += Mess[0]
        # 检查变量类型
        new_field = new_field + " C" + Mess[1][Mess[1].find('('):] + ";"
    # print(new_field)
    table = dbf.Table(filename=filename, field_specs=new_field, codepage='cp936')


# 删除表 by 王彦博
def DeleteTable(file, path):
    filename = path + '\\' + file + '.dbf'
    structfile = path + '\\' + file + '_struct.dbf'
    os.remove(filename)
    os.remove(structfile)
    tkinter.messagebox.showinfo("删除结果", "已成功删除表" + file + '!')

# 显示表
def ShowTable(file, path):
    filename = path + '\\' + file + '.dbf'
    structfile = path + '\\' + file + '_struct.dbf'
    contents = rd(filename)[1]
    titles = []
    titlemess = rd(structfile)[1]
    for i in titlemess:
        titles.append(i[0])
    show = [titles]
    show += contents
    return show


if __name__ == '__main__':
    '''f = 'user'
    b = 'B'
    s = [['name', 'varchar(6)', 'True', 'False'], ]
    CreateTable(f, s, b)'''
    print(ShowTable('test', 'B'))
