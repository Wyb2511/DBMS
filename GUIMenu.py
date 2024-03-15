import datetime
import pathlib
from queue import Queue
from threading import Thread
from tkinter.filedialog import askdirectory
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
from AboutTable import DeleteTable





if __name__ == '__main__':
    app = ttk.Window(title="DBMS",  # 设置窗口的标题
                     themename="cerculean",  # 设置主题
                     size=(1200, 800),  # 窗口的大小
                     position=(100, 100),  # 窗口所在的位置
                     minsize=(1000, 600),  # 窗口的最小宽高
                     # 窗口的最大宽高
                     resizable=None,  # 设置窗口是否可以更改大小
                     alpha=1.0, )
    # 3
    f = ttk.Frame(app)
    f.place(x=400, y=50, width=700, height=625)
    nb = ttk.Notebook(f)
    nb.pack(
        side=LEFT,
        padx=(10, 0),
        expand=YES,
        fill=BOTH
    )

    lf1 = ttk.Labelframe(text=" 请输入想删除的数据库信息", bootstyle=PRIMARY, width=700, height=500)
    lf1.place(x=10, y=50, width=700, height=500)
    t1 = ttk.Label(lf1, text="表名", bootstyle=INFO)
    t1.grid(padx=5, pady=10)
    table = ttk.Entry(lf1, width=50, show=None)
    # e1.insert('0',"默认插入内容")
    table.grid(row=5, column=1, sticky=ttk.W, padx=10, pady=10)
    t2 = ttk.Label(lf1, text="数据库名", bootstyle=INFO)
    t2.grid(padx=5, pady=10)
    database = ttk.Entry(lf1, width=50, bootstyle=PRIMARY)
    database.grid(row=10, column=1, sticky=ttk.W, padx=10, pady=10)


    def deletetable():
        DeleteTable(table.get(), database.get())


    ttk.Button(lf1, text="确认", bootstyle=(PRIMARY, "outline-toolbutton"), command=deletetable) \
        .grid(row=20, column=1, sticky=ttk.W, padx=400, pady=10)

    nb.add(
        lf1,
        text="  删除表  ",
        sticky=NW
    )

    nb.add(
        ttk.Button(nb, text="  描述文字  ", bootstyle=SUCCESS),
        text="  新建表  ",
        sticky=NW
    )

    nb.add(
        ttk.Button(nb, text="  描述文字  ", bootstyle=SUCCESS),
        text="  查询表  ",
        sticky=NW
    )

    nb.add(
        ttk.Button(nb, text="  描述文字  ", bootstyle=SUCCESS),
        text="  修改表  ",
        sticky=NW
    )

    app.mainloop()
