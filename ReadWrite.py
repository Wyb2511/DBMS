'''
把现有的dbf文件的数据，copy到一个指定的模板里面，并填充新增的项
'''
import re

import dbf


def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False


# 检查是否满足非空条件，如不满足就删除
def CheckNotNull(structfile, data):
    structs = rd(structfile)[1]
    indexList = []
    i = 0
    for struct in structs:
        if struct[2] == 'True':
            indexList.append(i)
        i += 1
    i = 0
    for k in indexList:
        if data[k] == '':
            return False
    return True


# 检查是否满足主码约束
def CheckKey(structfile, datafile, newdata):
    structs = rd(structfile)[1]
    datas = rd(datafile)[1]
    indexList = []
    i = 0
    for struct in structs:
        if struct[3] == 'True':
            indexList.append(i)
        i += 1
    count = len(indexList)
    for data in datas:
        for k in indexList:
            if newdata[k] == data[k]:
                count -= 1
        if count == 0:
            return False
    return True


def CheckKey_for_change(structfile, datafile, newdata, olddata):
    structs = rd(structfile)[1]
    datas = rd(datafile)[1]
    indexList = []
    i = 0
    for struct in structs:
        if struct[3] == 'True':
            indexList.append(i)
        i += 1
    count = len(indexList)
    i = 0
    print(datas)
    for data in datas:
        if data != olddata:
            count = len(indexList)
            for k in indexList:
                if newdata[k] == data[k]:
                    count -= 1
            if count == 0:
                return False
        else:
            datas[i] = newdata
        i += 1
    print(datas)
    return True


def cd(structfile, datafile):  # 根据结构文件检查数据
    structs = rd(structfile)[1]
    datas = rd(datafile)[1]
    i = 0
    for struct in structs:
        a = re.findall("\d+\.?\d*", struct[1])  # 正则表达式
        a = list(map(int, a))
        j = 0
        type = ''
        if 'int' in struct[1] or 'float' in struct[1]:
            type = 'number'
        elif 'varchar' in struct[1]:
            type = 'varchar'
        for data in datas:
            if len(data[i]) > a[0]:
                datas[j][i] = ''
            if type == 'number' and not is_number(datas[j][i]):
                datas[j][i] = ''
            j += 1
        i += 1
    new_field = ''
    for Mess in structs:
        new_field += Mess[0]
        # 检查变量类型
        new_field = new_field + " C" + Mess[1][Mess[1].find('('):] + ";"
    w(datafile, new_field, datas)


def w(file, field_specs, content):  # 写文件
    # 创建dbf文件
    table = dbf.Table(filename=file, field_specs=field_specs, codepage='cp936')
    # 修改为读写模式
    table.open(mode=dbf.READ_WRITE)
    for i in content:
        i = tuple(i)
        # print(i)
        table.append(i)
    table.close()


def rd(file):  # 读文件
    table = dbf.Table(
        filename=file,
        codepage='cp936',  # 相当于gbk的方式打开
    )
    table.open()
    tup = [[]]
    # L = len(table)
    j = 0
    # print(table.__len__())
    length = 0
    for row in table:
        # print(row)
        length = len(row)
        for i in range(length):
            tup[j].append(str.strip(str(row[i])))
        # print(tup)
        # print("------------------------")
        # tup[j] = tuple(tup[j])
        tup.append([])
        j += 1
    table.close()
    tup.pop(j)
    # print(tup)
    return length, tup


def Type(T):
    li = list(T)
    if li[0] == "v" and li[1] == "a" and li[2] == "r":
        l = r = 0
        for i in range(3, len(li)):
            if li[i] == "(":
                l = i
                for j in range(i, len(li)):
                    if li[j] == ")":
                        r = j
                        break
                break
        ans = "C("
        for i in range(l + 1, r):
            ans += li[i]
        ans += ")"
        return ans


if __name__ == '__main__':
    # print(rd('test_struct.dbf'))
    cd('B/test_struct.dbf', 'B/test.dbf')
    print(rd('B/test.dbf'))
'''
name C(25); type C(25); isNull C(5); isKey C(5)
'''
