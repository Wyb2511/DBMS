# -*- coding:utf-8 -*-
import os
import tkinter
import tkinter as tk
from functools import partial
from tkinter import *
from tkinter import messagebox
from DML import DMLDelete, delete_sql, insert_sql, DMLInsert
from DML import *
from AboutDatabase import DeleteDatabase, NewDatabase
from AboutTable import DeleteTable
from DDL import DDLCreateTable, DDLDropTable, DDLCreateDatabase, DDLDropDatabase
from Modification import DeleteStruct, AddStruct, ChangeStruct, DeleteData, AddData, ChangeData
from ReadWrite import rd, w

global state
global database
global table
global count
global num  # 记录输入数
state = 0
database = ''
table = ''
count = 0


def ShowDatabase():
    path = os.listdir(os.getcwd())
    databaselist = []
    for p in path:
        if os.path.isdir(p) and p != '.idea' and p != '__pycache__':
            databaselist.append(p)
    return databaselist


def ShowTables(DB):
    LIST = os.listdir(DB)
    i = 0
    dic = []
    for L in LIST:
        if '.dbf' in L and '_struct' not in L and 'NONE' not in L:
            dic.append(L.replace('.dbf', ''))
    return dic


def chooseDatabase(window, lb):
    # 使用 curselection来选中文本
    try:
        global database
        database = lb.get(lb.curselection())
        # database直接执行下一步
        ChangeState()
        window.destroy()
        showMenu()
    except Exception as e:
        e = '发现一个错误'
        messagebox.showwarning(e, '没有选择任何数据库')


def chooseTable(window, lb):
    try:
        global table
        table = lb.get(lb.curselection())
        # database直接执行下一步
        ChangeState()
        window.destroy()
        showMenu()
    except Exception as e:
        e = '发现一个错误'
        messagebox.showwarning(e, '没有选择任何表')


def ChangeState():
    global state
    if state != 2:
        state += 1


# 删除字段
def DeleteSelection(file, path):
    filename = path + '/' + file + '.dbf'
    structfile = path + '/' + file + '_struct.dbf'
    info_list = rd(structfile)[1]
    i = 30
    show_window = tk.Tk()
    show_window.title('删除字段')
    show_window.geometry('320x300')

    tk.Label(show_window, text='名              类型               是否NULL     键         ', bg='orange').pack()
    for temp_info in info_list:
        tk.Label(show_window, text=temp_info[0]).place(x=10, y=i)
        tk.Label(show_window, text=temp_info[1]).place(x=70, y=i)
        tk.Label(show_window, text=temp_info[2]).place(x=160, y=i)
        tk.Label(show_window, text=temp_info[3]).place(x=220, y=i)
        title = [temp_info[0], ]
        C = tk.Button(show_window, text="删除", command=partial(DeleteStruct, title, structfile, filename))
        C.pack()
        C.place(x=260, y=i, height=20, width=30)
        i += 30
    D = tk.Button(show_window, text="刷新", command=partial(renew, show_window, file, path))
    D.pack()
    D.place(x=140, y=i, height=20, width=30)


def ChangeSelection(file, path):
    filename = path + '/' + file + '.dbf'
    structfile = path + '/' + file + '_struct.dbf'
    info_list = rd(structfile)[1]
    i = 30
    show_window = tk.Tk()
    show_window.title('修改字段')
    show_window.geometry('320x300')
    EntryList = []
    k = 0
    tk.Label(show_window, text='名              类型               是否NULL     键         ', bg='orange').pack()
    for temp_info in info_list:
        EntryList.append([])
        # 放置输入框，并设置位置
        EntryList[k].append(tk.Entry(show_window))
        EntryList[k][0].pack()
        EntryList[k][0].place(x=10, y=i, width=50, height=30)
        EntryList[k][0].delete(0, "end")
        # 插入默认文本
        EntryList[k][0].insert(0, temp_info[0])

        EntryList[k].append(tk.Entry(show_window))
        EntryList[k][1].pack()
        EntryList[k][1].place(x=70, y=i, width=50, height=30)
        EntryList[k][1].delete(0, "end")
        # 插入默认文本
        EntryList[k][1].insert(0, temp_info[1])

        EntryList[k].append(tk.Entry(show_window))
        EntryList[k][2].pack()
        EntryList[k][2].place(x=130, y=i, width=50, height=30)
        EntryList[k][2].delete(0, "end")
        # 插入默认文本
        EntryList[k][2].insert(0, temp_info[2])

        EntryList[k].append(tk.Entry(show_window))
        EntryList[k][3].pack()
        EntryList[k][3].place(x=190, y=i, width=50, height=30)
        EntryList[k][3].delete(0, "end")
        # 插入默认文本
        EntryList[k][3].insert(0, temp_info[3])

        k += 1
        '''tk.Label(show_window, text=temp_info[0]).place(x=10, y=i)
        tk.Label(show_window, text=temp_info[1]).place(x=70, y=i)
        tk.Label(show_window, text=temp_info[2]).place(x=160, y=i)
        tk.Label(show_window, text=temp_info[3]).place(x=220, y=i)'''

        def GetStruct():
            StructList = []
            f = 0
            for line in EntryList:
                StructList.append([])
                for item in line:
                    StructList[f].append(item.get())
                f += 1
            try:
                Mess = ChangeStruct(structfile, filename, StructList)
                tkinter.messagebox.showinfo("修改结果", "已成功修改原字段" + Mess + '!')
            except Exception as e:
                e = '发现一个错误'
                messagebox.showwarning(e, '新增失败')

        C = tk.Button(show_window, text="修改", command=GetStruct)
        C.pack()
        C.place(x=260, y=i, height=20, width=30)
        i += 30

    def Renew():
        show_window.destroy()
        ChangeSelection(file, path)

    # D = tk.Button(show_window, text="刷新", command=Renew)
    # D = tk.Button(show_window, text="刷新", command=partial(DeleteSelection, file, path))
    # D.pack()


# 增加字段
def AddSelection(file, path, window):
    global count
    global num
    count = 0
    filename = path + '/' + file + '.dbf'
    structfile = path + '/' + file + '_struct.dbf'
    info_list = rd(structfile)[1]
    i = 30
    show_window = tk.Toplevel(window)
    show_window.title('增加字段')
    show_window.geometry('320x300')
    v = tk.IntVar()
    v.set(0)
    k = tk.IntVar()
    k.set(0)
    la = tk.IntVar()
    la.set(0)
    labe1 = tk.Label(show_window, text="字段名：")
    # grid()控件布局管理器，以行、列的形式对控件进行布局，后续会做详细介绍
    labe1.grid(row=0)
    name = tk.Entry(show_window)
    name.grid(row=0, column=1)

    # 类型就做选择吧
    labe2 = tk.Label(show_window, text="数据类型：")
    labe2.grid(row=2)
    q = tk.Radiobutton(show_window, text="int", variable=v, value=1)
    q.grid(row=2, column=1)
    p = tk.Radiobutton(show_window, text="float", variable=v, value=2)
    p.grid(row=3, column=1)
    r = tk.Radiobutton(show_window, text="varchar", variable=v, value=3)
    r.grid(row=4, column=1)

    labe3 = tk.Label(show_window, text="位数：")
    labe3.grid(row=5)
    length = tk.Entry(show_window)
    length.grid(row=6, column=1)

    # 非空也是选择
    labe4 = tk.Label(show_window, text="是否不可为空值：")
    labe4.grid(row=7)
    s = tk.Radiobutton(show_window, text="True", variable=k, value=1)
    s.grid(row=7, column=1)
    t = tk.Radiobutton(show_window, text="False", variable=k, value=2)
    t.grid(row=8, column=1)

    # 是否主码也是选择
    labe5 = tk.Label(show_window, text="是否主码：")
    labe5.grid(row=9)
    a = tk.Radiobutton(show_window, text="True", variable=la, value=1)
    a.grid(row=9, column=1)
    b = tk.Radiobutton(show_window, text="False", variable=la, value=2)
    b.grid(row=10, column=1)

    def ADD():
        try:
            l1 = ['int', 'float', 'varchar']
            l2 = ['True', 'False']
            AddStruct(structfile, filename, name.get(), l1[v.get() - 1] + '(' + length.get() + ')', l2[k.get() - 1],
                      l2[la.get() - 1])
            tkinter.messagebox.showinfo("修改结果", "已成功添加字段" + name.get() + '!')
        except Exception as e:
            e = '发现一个错误'
            messagebox.showwarning(e, '新增失败')

    tk.Button(show_window, text='新增字段', command=ADD).grid(row=11, column=1)


def renew(window, file, path):
    window.destroy()
    DeleteSelection(file, path)


def Deletedata(file, path):
    filename = path + '/' + file + '.dbf'
    structfile = path + '/' + file + '_struct.dbf'
    show_window = tk.Tk()
    show_window.title('删除行')
    show_window.geometry('320x300')
    info_list = rd(structfile)[1]
    num, info_list_1 = rd(filename)
    titlename = ''
    for temp_info in info_list:
        titlename += (temp_info[0] + '               ')
    la_0 = tk.Label(show_window, text=titlename, bg='yellow')
    la_0.pack()
    i = 30
    la_0.place(x=0, y=0)
    for temp_info in info_list_1:
        for k in range(num):
            tk.Label(show_window, text=temp_info[k]).place(x=0 + k * 90, y=i)
        C = tk.Button(show_window, text="删除", command=partial(DeleteData, structfile, filename, temp_info))
        C.pack()
        C.place(x=240, y=i, height=20, width=30)
        i += 20

    def renew_data():
        show_window.destroy()
        Deletedata(file, path)

    D = tk.Button(show_window, text="刷新", command=renew_data)
    D.pack()
    D.place(x=140, y=i, height=20, width=30)


def Adddata(file, path):
    filename = path + '/' + file + '.dbf'
    structfile = path + '/' + file + '_struct.dbf'
    show_window = tk.Tk()
    show_window.title('新增行')
    show_window.geometry('320x300')
    EntryList = []
    LabList = []
    structs = rd(structfile)[1]  # 属性信息
    N = len(structs)  # 属性个数
    for i in range(N):
        EntryList.append(tk.Entry(show_window))
        EntryList[i].grid(row=i, column=1)
        LabList.append(tk.Label(show_window, text=structs[i][0]))
        LabList[i].grid(row=i)

    def GetData():
        NewData = []
        for E in EntryList:
            NewData.append(E.get())
        if AddData(structfile, filename, NewData):
            tkinter.messagebox.showinfo("插入成功", "已成功新增行！")
        else:
            messagebox.showwarning('插入失败', '不满足约束！')

    tk.Button(show_window, text='新增数据', command=GetData).grid(row=i + 2, column=1)
    '''  labe1 = tk.Label(show_window, text="字段名：")
        # grid()控件布局管理器，以行、列的形式对控件进行布局，后续会做详细介绍
        labe1.grid(row=0)
        name = tk.Entry(show_window)
        name.grid(row=0, column=1)'''


def Changedata(file, path):
    filename = path + '/' + file + '.dbf'
    structfile = path + '/' + file + '_struct.dbf'
    show_window = tk.Tk()
    show_window.title('修改行')
    show_window.geometry('320x300')
    info_list = rd(structfile)[1]
    num, info_list_1 = rd(filename)
    titlename = ''
    for temp_info in info_list:
        titlename += (temp_info[0] + '               ')
    la_0 = tk.Label(show_window, text=titlename, bg='yellow')
    la_0.pack()
    i = 30
    la_0.place(x=0, y=0)
    for temp_info in info_list_1:
        for k in range(num):
            tk.Label(show_window, text=temp_info[k]).place(x=0 + k * 90, y=i)

        def change(mess):
            window = tk.Tk()
            window.title('行数据')
            window.geometry('320x300')
            EntryList = []
            t = 0
            for temp in info_list:
                tk.Label(window, text=temp[0] + ':').grid(row=t)
                EntryList.append(tk.Entry(window))
                EntryList[t].grid(row=t, column=2)
                EntryList[t].insert(0, mess[t])
                t += 1

                def Ch():
                    new = []
                    for E in EntryList:
                        new.append(E.get())

                    if ChangeData(mess, new, file, path):
                        tkinter.messagebox.showinfo("修改成功", "已成功修改行！")
                    else:
                        messagebox.showwarning('修改失败', '不满足约束！')

            tk.Button(window, text="提交", command=Ch).grid(row=t + 2, column=2)

        C = tk.Button(show_window, text="修改", command=partial(change, temp_info))
        C.pack()
        C.place(x=240, y=i, height=20, width=30)
        i += 20


#####################################
def GetSQL(txt):  #
    sql = txt.get("1.0", "end")  # 获取文本
    if "create" in sql.lower():  #
        if "table" in sql.lower():  #
            DDLCreateTable(sql)  #
        elif "database" in sql.lower():
            DDLCreateDatabase(sql)
    elif "drop" in sql.lower():
        if "table" in sql.lower() and "alter" not in sql.lower():
            DDLDropTable(sql)
        elif "table" in sql.lower() and "alter" in sql.lower():
            db = (sql.splitlines()[0].split()[1]).split(';')[0]
            gongneng(sql, db)
        elif "database" in sql.lower():
            DDLDropDatabase(sql)
    elif "insert" in sql.lower():
        db = (sql.splitlines()[0].split()[1]).split(';')[0]
        DMLInsert(insert_sql(sql), db)
    elif "select" in sql.lower():
        db = (sql.splitlines()[0].split()[1]).split(';')[0]
        tb = gongneng(sql, db)
        show_window = tk.Tk()
        show_window.title('查询结果')
        show_window.geometry('320x300')
        i = 30
        for temp_info in tb:
            if i == 30:
                c = 'yellow'
            else:
                c = 'white'
            k = 0
            for d in temp_info:
                tk.Label(show_window, text=d, bg=c).place(x=0 + k * 90, y=i)
                k += 1
            i += 30
    elif "update" in sql.lower():
        db = (sql.splitlines()[0].split()[1]).split(';')[0]
        gongneng(sql, db)
        tkinter.messagebox.showinfo("执行结果", "已执行！")
    elif "delete" in sql.lower():
        db = (sql.splitlines()[0].split()[1]).split(';')[0]
        DMLDelete(delete_sql(sql), db)
    elif "alter" in sql.lower():
        db = (sql.splitlines()[0].split()[1]).split(';')[0]
        gongneng(sql, db)

#####################################

def showMenu():
    if state == 0:
        root_window = tk.Tk()
        root_window.geometry('450x300')
        root_window.title('DBMS')
        # 右边的组件
        # 调用Tk()创建主窗口
        var1 = tk.StringVar()
        text = tk.Text(root_window, width=30, height=18)
        text.pack()
        text.place(x=200, y=20)

        button = tk.Button(root_window, text="执行查询", command=partial(GetSQL, text))
        # 将按钮放置在主窗口内
        button.pack(side="bottom")

        # 左边的组件
        lb = Listbox(root_window)
        lb.pack(side=LEFT)
        lb.place(x=0, y=70)
        # i表示索引值，item 表示值，根据索引值的位置依次插入
        databases = ShowDatabase()
        for i, item in enumerate(databases):
            lb.insert(i, item)
        b1 = tk.Button(root_window, text='选择当前数据库', command=partial(chooseDatabase, root_window, lb))
        b1.pack()
        b1.place(x=5, y=15, height=20, width=135)

        def newdb():
            show_window = tk.Tk()
            show_window.title('新建数据库')
            show_window.geometry('320x300')
            e = tk.Entry(show_window)
            e.pack()

            def getdb():
                NewDatabase(e.get())
                tkinter.messagebox.showinfo("新建数据库", "已成功建立数据库" + e.get() + '!')

            tk.Button(show_window, text='确定', command=getdb).pack()

        b2 = tk.Button(root_window, text='新建数据库', command=newdb)
        b2.pack()
        b2.place(x=5, y=50, height=20, width=135)
        root_window.mainloop()
    elif state == 1:
        root_window = tk.Tk()
        root_window.geometry('450x300')
        root_window.title('DBMS')
        # 左边的组件

        lb_1 = Listbox(root_window)
        lb_1.pack(side=LEFT)
        lb_1.place(x=0, y=70)
        # i表示索引值，item 表示值，根据索引值的位置依次插入
        global database
        tables = ShowTables(database)
        for i, item in enumerate(tables):
            lb_1.insert(i, item)
        b1 = tk.Button(root_window, text='选择表', command=partial(chooseTable, root_window, lb_1))
        b1.pack()
        b1.place(x=5, y=10, height=20, width=135)
        b0 = tk.Button(root_window, text='删除数据库', command=partial(DeleteDatabase, database))
        b0.pack()
        b0.place(x=5, y=40, height=20, width=135)
        # 将按钮放置在主窗口内
        # 开启主循环，让窗口处于显示状态
        root_window.mainloop()
    elif state == 2:
        root_window = tk.Tk()
        root_window.geometry('600x300')
        root_window.title('DBMS3')
        # 左边的组件
        filename = database + '/' + table + '.dbf'
        structfile = database + '/' + table + '_struct.dbf'
        i = 30
        info_list = rd(structfile)[1]
        num, info_list_1 = rd(filename)
        titlename = ''
        la_0 = tk.Label(root_window, text='名              类型               是否NULL     键         ', bg='orange')
        la_0.pack()
        la_0.place(x=10, y=0)
        for temp_info in info_list:
            titlename += (temp_info[0] + '               ')
            tk.Label(root_window, text=temp_info[0]).place(x=10, y=i)
            tk.Label(root_window, text=temp_info[1]).place(x=70, y=i)
            tk.Label(root_window, text=temp_info[2]).place(x=160, y=i)
            tk.Label(root_window, text=temp_info[3]).place(x=220, y=i)
            i += 20
        la_0 = tk.Label(root_window, text=titlename, bg='yellow')
        la_0.pack()
        i = 30
        la_0.place(x=320, y=0)
        for temp_info in info_list_1:
            for k in range(num):
                tk.Label(root_window, text=temp_info[k]).place(x=320 + k * 90, y=i)
            i += 20
        # 将按钮放置在主窗口内
        # 开启主循环，让窗口处于显示状态
        b_1 = tk.Button(root_window, text='新增字段', command=partial(AddSelection, table, database, root_window))
        b_1.pack()
        b_1.place(x=20, y=250)
        b_2 = tk.Button(root_window, text='删除字段', command=partial(DeleteSelection, table, database))
        b_2.pack()
        b_2.place(x=100, y=250)
        b_3 = tk.Button(root_window, text='修改字段', command=partial(ChangeSelection, table, database))
        b_3.pack()
        b_3.place(x=180, y=250)
        b_4 = tk.Button(root_window, text='删除数据', command=partial(Deletedata, table, database))
        b_4.pack()
        b_4.place(x=260, y=250)
        b_5 = tk.Button(root_window, text='增加数据', command=partial(Adddata, table, database))
        b_5.pack()
        b_5.place(x=340, y=250)
        b_6 = tk.Button(root_window, text='修改数据', command=partial(Changedata, table, database))
        b_6.pack()
        b_6.place(x=420, y=250)

        def renewtable():
            root_window.destroy()
            showMenu()

        b_7 = tk.Button(root_window, text='刷新', command=renewtable)
        b_7.pack()
        b_7.place(x=500, y=250)

        b_8 = tk.Button(root_window, text='删除表', command=partial(DeleteTable, table, database))
        b_8.pack()
        b_8.place(x=550, y=250)

        def back():
            global state
            global database
            global table
            global count
            state = 0
            database = ''
            table = ''
            count = 0
            root_window.destroy()
            showMenu()

        b_9 = tk.Button(root_window, text='返回', command=back)
        b_9.pack()
        b_9.place(x=570, y=10)
        root_window.mainloop()


if __name__ == '__main__':
    showMenu()
