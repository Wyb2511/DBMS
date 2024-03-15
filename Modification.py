from operator import eq

from ReadWrite import w, rd, Type, cd, CheckKey, CheckNotNull, CheckKey_for_change


# by 郑钧泽 & 赖楚韬
# 下面两个文件是对数据进行修改，分别是增加和删除
def AddData(structfile, file, content):
    if CheckKey(structfile, file, content) and CheckNotNull(structfile, content):
        l0, tup0 = rd(structfile)
        new_field = ''
        l1, tup1 = rd(file)
        tup1.append(content)
        for Mess in tup0:
            new_field += Mess[0]
            # 检查变量类型
            new_field = new_field + " C" + Mess[1][Mess[1].find('('):] + ";"
        w(file, new_field, tup1)
        return True
    else:
        return False


def ChangeData(oldline, newline, file, path):
    print(newline)
    datafile = path + '/' + file + '.dbf'
    structfile = path + '/' + file + '_struct.dbf'
    contents = rd(datafile)[1]
    i = 0
    for content in contents:
        if content == oldline:
            contents[i] = newline
            break
        i += 1
    TitleMess = rd(structfile)[1]
    new_field = ''
    for Mess in TitleMess:
        new_field += Mess[0]
        # 检查变量类型
        new_field = new_field + " C" + Mess[1][Mess[1].find('('):] + ";"
    if CheckKey_for_change(structfile, datafile, newline, oldline) and CheckNotNull(structfile, newline):
        w(datafile, new_field, contents)
        return True
    else:
        contents[i] = oldline
        w(datafile, new_field, contents)
        return False


def DeleteData(structfile, file, content):  # 删除数据
    l0, tup0 = rd(structfile)
    l1, tup1 = rd(file)
    for i in tup1:
        if eq(content, i):
            tup1.remove(i)
    new_field = ''
    for Mess in tup0:
        new_field += Mess[0]
        # 检查变量类型
        new_field = new_field + " C" + Mess[1][Mess[1].find('('):] + ";"
    w(file, new_field, tup1)


# 下面两个分别是增加字段和删除字段
def AddStruct(structfile, file, name, type0, notNull, isKey):
    l0, tup0 = rd(structfile)
    tup0.append([name, type0, notNull, isKey])
    w(structfile, "name C(25); type C(25); notNull C(5); isKey C(5)", tup0)  # 重新写结构文件
    l1, tup1 = rd(file)
    for i in range(len(tup1)):
        tup1[i].append("")
    new_field = ''
    for Mess in tup0:
        new_field += Mess[0]
        # 检查变量类型
        new_field = new_field + " C" + Mess[1][Mess[1].find('('):] + ";"
    w(file, new_field, tup1)  # 给数据文件占位


def DeleteStruct(titles, filename, datafilename):  # titles为列表，存放要删除的属性名，filename为结构文件名，datafilename为数据文件名
    # 先修改表结构
    num = []  # 存放下标信息
    TitleMess = rd(filename)[1]  # 存放每一个字段信息
    for Name in titles:
        # 先找到Name对应的下标
        for Mess in TitleMess:
            if Mess[0] == Name:
                num.append(TitleMess.index(Mess))
                TitleMess.remove(Mess)
    w(filename, 'name C(25);type C(25);isNull C(5);isKey C(5)', TitleMess)
    new_field = ''
    for Mess in TitleMess:
        new_field += Mess[0]
        # 检查变量类型
        new_field = new_field + " C" + Mess[1][Mess[1].find('('):] + ";"
    # 然后修改表数据
    DataMess = rd(datafilename)[1]
    for Data in DataMess:
        for k in num:
            del Data[k]
    # print(DataMess)
    w(datafilename, new_field, DataMess)


def ChangeStruct(filename, datafilename, newstr):  # titles为列表，存放要删除的属性名，filename为结构文件名，datafilename为数据文件名
    oldstr = rd(filename)[1]
    num = len(oldstr)
    w(filename, 'name C(25);type C(25);isNull C(5);isKey C(5)', newstr)
    cd(filename, datafilename)
    change = ''
    for i in range(num):
        if not eq(oldstr[i], newstr[i]):
            change += oldstr[i][0] + ' '
    return change


def UpDate(structfile, file, neirong):  # 覆写数据
    l0, tup0 = rd(structfile)
    new_field = ""
    tup1 = []
    for i in neirong:
        tup1.append(i)
    for Mess in tup0:
        new_field += Mess[0]
        # 检查变量类型
        new_field = new_field + " C" + Mess[1][Mess[1].find('('):] + ";"
    w(file, new_field, tup1)


if __name__ == '__main__':
    '''print(rd('test.dbf'))
    DeleteStruct(["age", ], 'test_struct.dbf', 'test.dbf')
    print(rd('test_struct.dbf'))
    print(rd('test.dbf'))'''
    print(rd('B//test.dbf'))
    ChangeData(['xiao', '18'], ['xia', '18'], 'test', 'B')
    print(rd('B//test.dbf'))
