import re
import cha as where0
import ReadWrite as rw
# from ReadWrite import w, rd, Type
from Modification import DeleteData, UpDate, AddData
import re
import cha as c  # c代表查
import gai as g  # g代表改
import ReadWrite as rw
import paixu as PX
import se8
import Modification as mf
import Alter as al


# 测试用例
# delete  from 测试 where 属性1 = 'Gates'
# delete  from 测试
# --------------------------------
# delete from, where
# ([1, 1])

# by 薛李丹
def delete_sql(sql):
    # li0 = []
    # 匹配where后面的,调用查询模块
    if re.search(r'(where|WHERE).*', sql):
        where0.where0(sql, 0)
        # li0.append(where0.where0(sql, 0))
    # 匹配from后面的,如果from后面有where子句则执行if语句，否则执行后者
    if re.search(r'(from|FROM).*(where|WHERE)', sql):
        ans0 = re.search(r'(from|FROM).*(where|WHERE)', sql)
        ans0 = re.sub(r'delete|DELETE|from|FROM|where|WHERE|\s', '', ans0.group())
        ans0 = re.split(r',', ans0)
        print(ans0)
        # li0.append(ans0)
        # li = {"from": ans0, "where": where0.where0(sql, 0)}
    else:
        # if re.search(r'(from|FROM).*', sql):
        ans1 = re.search(r'(from|FROM).*', sql)
        ans1 = re.sub(r'delete|DELETE|from|FROM|\s', '', ans1.group())
        ans1 = re.split(r',', ans1)
        print(ans1)
        # li = {"from": ans1}
        # li0.append(ans1)

    if re.search(r'(from|FROM).*(where|WHERE)', sql):
        li = {"from": ans0, "where": where0.where0(sql, 0)}
    else:
        li = {"from": ans1}

    return li
    # 调用函数
    # DeleteData(structfile, file, li0)


# use, select, from, where, group by, order by
# (str, [0/1/2/3, [1, 1, 1, 1, 0, 0]])
# 0:普通条件
# 1:空值判断 name is null [1, ['name', 'is'], 0] , [1, ['name', 'is not'], 0]
# 2:in判断 sal in (5000,3000,1500) [2, ['sal', 3, ['5000', '3000', '1500'], 0]]
# 3:like判断 ename like 'M%' [3, ['ename', 'M%'], 0]
# 4:between
#
# [['test'], ['id', 'name'], ['table1'], [[0,['id', '=', '0'], 1], [0, ['name', '=', 'zzz'], 2], [0, ['id1', '=', '2'], 0]], [], []]
#
# 0:后面为空
# 1:后面为and
# 2:后面为or
# -----------------------------------------------
# 删除模块的大致思路：
#   1：先匹配对应from值，也就是对应的表
#   2：有两种情况，一种是删除某些指定行，也就是有where子句时，从中判断选择符合条件的语句
#               另一种是删除所有行
#   问题：a.怎么删除表的内容，表的全部内容可以读取file文件实现全部删除，
#        b.表的部分内容，也就是符合where子句条件的数据，怎么删除
#           先把表的内容全部取出，然后删除符合条件的数据，再覆盖写回
# -----------------------------------------------------
# 1选出符合where条件的
# 2利用python list pop方法删除符合条件的


def DMLDelete(zd, db):
    # 1读取对应的表的全部内容以及表结构
    file = db + '/' + zd['from'][0] + '.dbf'
    structfile = db + '/' + zd['from'][0] + '_struct.dbf'
    f_l, f_rd = rw.rd(file)
    sf_l, sf_rd = rw.rd(structfile)

    # print(ans)
    sf_zd = {}
    sf_lx = []
    for i in range(len(sf_rd)):
        sf_zd[sf_rd[i][0]] = i
        sf_lx.append(sf_rd[i][1])
    # 特殊符号的转换
    for i in range(f_l):
        if re.search(r'int', sf_lx[i]) is not None:
            for j in range(len(f_rd)):
                f_rd[j][i] = int(f_rd[j][i])
        elif re.search(r'float', sf_lx[i]) is not None:
            for j in range(len(f_rd)):
                f_rd[j][i] = float(f_rd[j][i])

    for i in range(len(f_rd)):  # 遍历记录
        f_rd[i].append(0)
    flag = 0
    # 判断对应的表是否为删除某些行,并将符合条件的记录筛选出来
    if zd['where'] is not None:
        panduan = zd['where']
        flag += 1
        for pd in panduan:
            pd[1][2] = pd[1][2].strip('`')
            if pd[0] == 0:  # 普通条件
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    pd[1][2] = int(pd[1][2])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    pd[1][2] = float(pd[1][2])

                if pd[1][1] == '=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '!=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '>':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] > pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '<':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] < pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '>=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] >= pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '<=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] <= pd[1][2]:
                            f_rd[i][f_l] += 1
            elif pd[0] == 1:  # 空值判断
                if pd[1][1] == 'is':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == '':
                            f_rd[i][f_l] += 1
                elif pd[1][1] == 'is not':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != '':
                            f_rd[i][f_l] += 1
            elif pd[0] == 2:  # in判断
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = int(pd[1][1][i])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = float(pd[1][1][i])
                for i in range(len(f_rd)):
                    if f_rd[i][sf_zd[pd[1][0]]] in pd[1][1]:
                        f_rd[i][f_l] += 1
            elif pd[0] == 3:  # like判断
                if re.search(r'%', pd[1][1]) is None:
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][1]:
                            f_rd[i][f_l] += 1
                else:
                    like0 = re.sub(r'%', '.*', pd[1][1])
                    if re.search(r'^%', pd[1][1]) is not None:
                        like0 = '^' + like0
                        if re.search(r'\^\.\*', like0) is not None:
                            like0 = re.sub(r'\^\.\*', '^.+', like0)
                    if re.search(r'%$', pd[1][1]) is not None:
                        like0 = like0 + '$'
                        if re.search(r'\.\*\$', like0) is not None:
                            like0 = re.sub(r'\.\*\$', '.+$', like0)
                    like1 = r'{}'.format(like0)
                    # print(like1)
                    for i in range(len(f_rd)):
                        if re.search(like1, f_rd[i][sf_zd[pd[1][0]]]) is not None:
                            f_rd[i][f_l] += 1

            if pd[2] == 1:
                flag += 1
        ans0 = []
        for i in range(len(f_rd)):
            if f_rd[i][f_l] < flag:
                f_rd[i].pop(f_l)
                ans0.append(f_rd[i])  # 符合条件的语句，pop取出符合条件的记录后f_rd是保存后的语句
        i = 0
        j = 0
        for i in range(len(ans0)):
            for j in range(len(ans0[i])):
                ans0[i][j] = str(ans0[i][j])
                j += 1
            i += 1
        print(ans0)
        UpDate(structfile, file, ans0)
    # 3覆盖写入

    # 否则删除表的全部内容
    else:
        DeleteData(structfile, file, rw.rd(file))


# 对插入语句进行语义分析
def insert_sql(sql):
    # tq = "INSERT INTO Persons (LastName, Address) VALUES ('Wilson', 'Champs-Elysees')"
    # 如果检测到插入表的属性(),就进行特殊处理,否则就普通处理
    # li0 = []
    if re.search(r'\)\s+(value|VALUE)', sql):
        # 处理括号外的
        ans = re.search(r'(insert|INSERT)\s+(into|INTO).*\(', sql)
        ans = re.search(r'(insert|INSERT)\s+(into|INTO).*\)', ans.group())
        ans = re.search(r'(insert|INSERT)\s+(into|INTO).*\(', ans.group())
        ans = re.sub(r'insert|INSERT|into|INTO|\(|\s', '', ans.group())
        ans = re.split(r',', ans)

        # 处理括号内的
        ans1 = re.search(r'(insert|INSERT)\s+(into|INTO).*\(', sql)
        ans1 = re.search(r'\(.*', ans1.group())
        ans1 = re.sub(r'\(|values|VALUES|\)|\s', '', ans1.group())
        ans1 = re.split(r',', ans1)
        # print(ans)
        # print(ans1)
        # li0.append(ans)
        # li0.append(ans1)
    else:
        ans0 = re.search(r'(insert|INSERT).*(values|VALUES)', sql)
        # print("初次匹配:", ans0.group())
        ans0 = re.sub(r'insert|INSERT|into|INTO|values|VALUES|\s', '', ans0.group())
        # print("去除多余内容:", ans0)
        ans0 = re.split(r',', ans0)
        # print(ans0)
        # li0.append(ans0)

    # 再次匹配value
    ans2 = re.search(r'(values|VALUES).*', sql)
    if ans2:
        # print("再次匹配:", ans2.group())
        # 去除多余内容
        ans2 = re.sub(r'values|VALUES|\'|\"|\(|\)|\s', '', ans2.group())
        # print("去除多余内容:", ans2)
        # 提取内容
        ans2 = re.split(r',', ans2)
        # print(ans2)
        # li0.append(ans2)
    # 如果特殊处理就特殊传送
    if re.search(r'\)\s+(value|VALUE)', sql):
        li = {"insertinto": ans, "titles": ans1, "values": ans2}
    else:
        li = {"insertinto": ans0, "values": ans2}

    # print(li0)
    return li


# 测试样例
# INSERT INTO test VALUES ('Gates', 'Bill', 'Xuanwumen 10', 'Beijing')
# INSERT INTO test(LastName, Address) VALUES ('Wilson', 'Champs-Elysees')

# 插入语句的大致思路是
# 1判断是否为部分插入，如果是；
#   读取（from）表名对应的表头属性到一个新的列表中，用tup0[i][0] in ans判断表头属性是否存在，
#   如果存在则将zd['values']的值赋给value列表
#   如果不存在则用‘’赋值给value列表占位
# 处理完成后values的值可以直接按照全部插入处理
# 2如果是全部插入处理，直接读取insertinto后表名，再对应的表名中插入属性值（处理values）
# -----------------------------------------------------------------

'''sql = input("请输入插入语句：")
t1 = insert_sql(sql)
print(t1)'''


def DMLInsert(dic, path):
    # 读取对应的表
    file = path + '/' + dic['insertinto'][0] + '.dbf'
    structfile = path + '/' + dic['insertinto'][0] + '_struct.dbf'
    l0, tup0 = rw.rd(structfile)  # 表头属性读取
    # 判断对应的表是否为部分插入
    if len(dic['titles']) < len(tup0):
        ans = dic['titles']
        print(tup0)
        print(ans)
        a = dic['values']
        # print(ans)
        # print(ans0)
        # 表的占位，
        # 建立一个新的value列表，如果表的属性在zd['shuxing']里面，则用输入对应的属性值zd['values']
        # 如果不在，则用‘’占位

        value = []

        # 对value列表初始化
        for i in range(len(tup0)):
            if tup0[i][0] in ans:
                value.append(a[ans.index(tup0[i][0])])
            else:
                value.append('')
        print(value)
        # ans0 = np.array(value)
        # print('0--------------')
        # print(value)
        for tup0[i][0] in ans:
            ans0 = np.array(a)
            # ans0 = zd['shuxing']
            # print('1--------------')
            # print(ans0)
            value[i] = ans0
    else:
        # 否则是全部插入，调用插入函数直接插入数据
        value = dic['values']
    return AddData(structfile, file, value)


# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥

# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥

# by 郑钧泽
# use, select, from, where, group by, order by
# (str, [0/1/2/3, [1, 1, 1, 1, 0, 0]])
# 0:普通条件
# 1:空值判断 name is null [1, ['name', 'is'], 0] , [1, ['name', 'is not'], 0]
# 2:in判断 sal in (5000,3000,1500) [2, ['sal', 3, ['5000', '3000', '1500'], 0]]
# 3:like判断 ename like 'M%' [3, ['ename', 'M%'], 0]
# 4:between
#
# [['test'], ['id', 'name'], ['table1'], [[0,['id', '=', '0'], 1], [0, ['name', '=', 'zzz'], 2], [0, ['id1', '=', '2'], 0]], [], []]
#
# 0:后面为空
# 1:后面为and
# 2:后面为or
def chaxun(zd, db):
    ans = [[]]
    file = zd['from'][0] + '.dbf'
    structfile = zd['from'][0] + '_struct.dbf'
    f_l, f_rd = rw.rd(db + '/' + file)
    sf_l, sf_rd = rw.rd(db + '/' + structfile)
    if zd['select'] != ['*']:
        ans = [zd['select']]
    else:
        for i in sf_rd:
            ans[0].append(i[0])
    # print(ans)
    sf_zd = {}
    sf_lx = []
    for i in range(len(sf_rd)):
        sf_zd[sf_rd[i][0]] = i
        sf_lx.append(sf_rd[i][1])
    for i in range(f_l):
        if re.search(r'int', sf_lx[i]) is not None:
            for j in range(len(f_rd)):
                if f_rd[j][i] != '':
                    f_rd[j][i] = int(f_rd[j][i])
        elif re.search(r'float', sf_lx[i]) is not None:
            for j in range(len(f_rd)):
                if f_rd[j][i] != '':
                    f_rd[j][i] = float(f_rd[j][i])

    for i in range(len(f_rd)):  # 遍历记录
        f_rd[i].append(0)
    flag = 0
    if zd['where'] is not None:
        panduan = zd['where']
        flag += 1
        for pd in panduan:
            if pd[0] == 0:  # 普通条件
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    pd[1][2] = int(pd[1][2])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    pd[1][2] = float(pd[1][2])

                if pd[1][1] == '=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '!=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '>':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] > pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '<':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] < pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '>=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] >= pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '<=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] <= pd[1][2]:
                            f_rd[i][f_l] += 1
            elif pd[0] == 1:  # 空值判断
                if pd[1][1] == 'is':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == '':
                            f_rd[i][f_l] += 1
                elif pd[1][1] == 'is not':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != '':
                            f_rd[i][f_l] += 1
            elif pd[0] == 2:  # in判断
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = int(pd[1][1][i])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = float(pd[1][1][i])
                for i in range(len(f_rd)):
                    if f_rd[i][sf_zd[pd[1][0]]] in pd[1][1]:
                        f_rd[i][f_l] += 1
            elif pd[0] == 3:  # like判断
                if re.search(r'%', pd[1][1]) is None:
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][1]:
                            f_rd[i][f_l] += 1
                else:
                    like0 = re.sub(r'%', '.*', pd[1][1])
                    if re.search(r'^%', pd[1][1]) is not None:
                        like0 = '^' + like0
                        if re.search(r'\^\.\*', like0) is not None:
                            like0 = re.sub(r'\^\.\*', '^.+', like0)
                    if re.search(r'%$', pd[1][1]) is not None:
                        like0 = like0 + '$'
                        if re.search(r'\.\*\$', like0) is not None:
                            like0 = re.sub(r'\.\*\$', '.+$', like0)
                    like1 = r'{}'.format(like0)
                    # print(like1)
                    for i in range(len(f_rd)):
                        if re.search(like1, f_rd[i][sf_zd[pd[1][0]]]) is not None:
                            f_rd[i][f_l] += 1

            if pd[2] == 1:
                flag += 1
            # print(f_rd)
    ans0 = []
    ans1 = []
    for i in range(len(f_rd)):
        if f_rd[i][f_l] >= flag:
            f_rd[i].pop(f_l)
            ans0.append(f_rd[i])
            ans1.append([])
    # chaxun = zd['select']
    # cx = []
    # for i in chaxun:
    #     cx.append(sf_zd[i])

    if zd['orderby'] is not None:
        paixu = zd['orderby']
        l_p = len(paixu)
        flag_p = 1
        if paixu[l_p - 1] in ['asc', 'ASC', 'desc', 'DESC']:
            if paixu[l_p - 1] in ['desc', 'DESC']:
                flag_p = 0
            paixu.pop(l_p - 1)
            l_p -= 1
        for i in range(l_p):
            paixu[i] = sf_zd[paixu[i]]
        if flag_p == 1:
            PX.upsort(ans0, 0, len(ans0) - 1, paixu)
        else:
            PX.downsort(ans0, 0, len(ans0) - 1, paixu)
    # print(ans[0])
    chaxun0 = ans[0]
    for i in chaxun0:
        for j in range(len(ans0)):
            ans1[j].append(ans0[j][sf_zd[i]])
    ans += ans1
    return ans


def xiugai(zd, db):
    file = db + '/' + zd['update'][0] + '.dbf'
    structfile = db + '/' + zd['update'][0] + '_struct.dbf'
    f_l, f_rd = rw.rd(file)
    sf_l, sf_rd = rw.rd(structfile)

    sf_zd = {}
    sf_lx = []
    for i in range(len(sf_rd)):
        sf_zd[sf_rd[i][0]] = i
        sf_lx.append(sf_rd[i][1])
    for i in range(f_l):
        if re.search(r'int', sf_lx[i]) is not None:
            for j in range(len(f_rd)):
                if f_rd[j][i] != '':
                    f_rd[j][i] = int(f_rd[j][i])
        elif re.search(r'float', sf_lx[i]) is not None:
            for j in range(len(f_rd)):
                if f_rd[j][i] != '':
                    f_rd[j][i] = float(f_rd[j][i])

    for i in range(len(f_rd)):  # 遍历记录
        f_rd[i].append(0)
    flag = 0
    if zd['where'] is not None:
        panduan = zd['where']
        flag += 1
        for pd in panduan:
            if pd[0] == 0:  # 普通条件
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    if pd[1][2] != '':
                        pd[1][2] = int(pd[1][2])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    if pd[1][2] != '':
                        pd[1][2] = float(pd[1][2])

                if pd[1][1] == '=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '!=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '>':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] > pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '<':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] < pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '>=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] >= pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '<=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] <= pd[1][2]:
                            f_rd[i][f_l] += 1
            elif pd[0] == 1:  # 空值判断
                if pd[1][1] == 'is':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == '':
                            f_rd[i][f_l] += 1
                elif pd[1][1] == 'is not':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != '':
                            f_rd[i][f_l] += 1
            elif pd[0] == 2:  # in判断
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = int(pd[1][1][i])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = float(pd[1][1][i])
                for i in range(len(f_rd)):
                    if f_rd[i][sf_zd[pd[1][0]]] in pd[1][1]:
                        f_rd[i][f_l] += 1
            elif pd[0] == 3:  # like判断
                if re.search(r'%', pd[1][1]) is None:
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][1]:
                            f_rd[i][f_l] += 1
                else:
                    like0 = re.sub(r'%', '.*', pd[1][1])
                    if re.search(r'^%', pd[1][1]) is not None:
                        like0 = '^' + like0
                        if re.search(r'\^\.\*', like0) is not None:
                            like0 = re.sub(r'\^\.\*', '^.+', like0)
                    if re.search(r'%$', pd[1][1]) is not None:
                        like0 = like0 + '$'
                        if re.search(r'\.\*\$', like0) is not None:
                            like0 = re.sub(r'\.\*\$', '.+$', like0)
                    like1 = r'{}'.format(like0)
                    # print(like1)
                    for i in range(len(f_rd)):
                        if re.search(like1, f_rd[i][sf_zd[pd[1][0]]]) is not None:
                            f_rd[i][f_l] += 1

            if pd[2] == 1:
                flag += 1

    xiugai0 = zd['set']
    ans0 = []
    ans1 = []
    # print(f_rd)
    for i in range(len(f_rd)):
        if f_rd[i][f_l] >= flag:
            for j in xiugai0:
                f_rd[i][sf_zd[j[0]]] = j[2]
        f_rd[i].pop(f_l)
        # ans0.append(f_rd[i])
        # ans1.append([])
    # print(f_rd)
    mf.UpDate(structfile, file, f_rd)


def duo_chaxun(zd, db):
    ans = [[]]
    f_l = []
    f_rd = []
    sf_l = []
    sf_rd = []
    sign = 0
    for i in zd['from']:
        res = rw.rd(db + '/' + i + '.dbf')
        f_l.append(res[0])
        f_rd.append(res[1])
        res = rw.rd(db + '/' + i + '_struct.dbf')
        sf_l.append(res[0])
        sf_rd.append(res[1])

    if zd['select'] != ['*']:
        ans = [zd['select']]
    else:
        sign = 1
        # for i in sf_rd:
        #     ans[0].append(i[0])

    sf_zd = {}  # 属性-下标字典
    sf_lx = []  # 属性类型
    b_len = 0
    for i in range(len(sf_rd)):
        for j in range(len(sf_rd[i])):
            sf_zd[sf_rd[i][j][0]] = b_len
            sf_zd[zd['from'][i] + '.' + sf_rd[i][j][0]] = b_len
            if sign == 1:
                ans[0].append(zd['from'][i] + '.' + sf_rd[i][j][0])
            sf_lx.append(sf_rd[i][j][1])
            b_len += 1

    b_len0 = 0
    for i in range(len(f_l)):
        for j in range(f_l[i]):
            if re.search(r'int', sf_lx[b_len0]) is not None:
                for k in range(len(f_rd[i])):
                    if f_rd[i][k][j] != '':
                        f_rd[i][k][j] = int(f_rd[i][k][j])
            elif re.search(r'float', sf_lx[b_len0]) is not None:
                for k in range(len(f_rd[i])):
                    if f_rd[i][k][j] != '':
                        f_rd[i][k][j] = float(f_rd[i][k][j])
            b_len0 += 1

    for i in range(len(f_rd)):  # 多表连接
        if i == 0:
            biao = f_rd[0].copy()
            biao0 = []
        else:
            b_h = len(biao)
            for j in range(b_h):
                for k in range(len(f_rd[i])):
                    biao0.append(biao[j] + f_rd[i][k])
            biao = biao0.copy()
            biao0 = []

    b_h = len(biao)
    for i in range(b_h):  # 遍历记录
        biao[i].append(0)

    flag = 0
    f_rd = biao
    f_l = b_len
    if zd['where'] is not None:
        panduan = zd['where']
        flag += 1
        for pd in panduan:
            # print(pd)
            if pd[0] == 0:  # 普通条件
                if pd[1][2] not in sf_zd.keys():
                    if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                        pd[1][2] = int(pd[1][2])
                    elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                        pd[1][2] = float(pd[1][2])

                    if pd[1][1] == '=':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] == pd[1][2]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '!=':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] != pd[1][2]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '>':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] > pd[1][2]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '<':
                        for i in range(len(f_rd)):
                            # print(f_rd[i][sf_zd[pd[1][0]]], pd[1][2])
                            if f_rd[i][sf_zd[pd[1][0]]] < pd[1][2]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '>=':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] >= pd[1][2]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '<=':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] <= pd[1][2]:
                                f_rd[i][f_l] += 1
                else:
                    if pd[1][1] == '=':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] == f_rd[i][sf_zd[pd[1][2]]]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '!=':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] != f_rd[i][sf_zd[pd[1][2]]]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '>':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] > f_rd[i][sf_zd[pd[1][2]]]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '<':
                        for i in range(len(f_rd)):
                            # print(f_rd[i][sf_zd[pd[1][0]]], f_rd[i][sf_zd[pd[1][2]]])
                            if f_rd[i][sf_zd[pd[1][0]]] < f_rd[i][sf_zd[pd[1][2]]]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '>=':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] >= f_rd[i][sf_zd[pd[1][2]]]:
                                f_rd[i][f_l] += 1
                    elif pd[1][1] == '<=':
                        for i in range(len(f_rd)):
                            if f_rd[i][sf_zd[pd[1][0]]] <= f_rd[i][sf_zd[pd[1][2]]]:
                                f_rd[i][f_l] += 1
            elif pd[0] == 1:  # 空值判断
                if pd[1][1] == 'is':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == '':
                            f_rd[i][f_l] += 1
                elif pd[1][1] == 'is not':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != '':
                            f_rd[i][f_l] += 1
            elif pd[0] == 2:  # in判断
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = int(pd[1][1][i])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = float(pd[1][1][i])
                for i in range(len(f_rd)):
                    if f_rd[i][sf_zd[pd[1][0]]] in pd[1][1]:
                        f_rd[i][f_l] += 1
            elif pd[0] == 3:  # like判断
                if re.search(r'%', pd[1][1]) is None:
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][1]:
                            f_rd[i][f_l] += 1
                else:
                    like0 = re.sub(r'%', '.*', pd[1][1])
                    if re.search(r'^%', pd[1][1]) is not None:
                        like0 = '^' + like0
                        if re.search(r'\^\.\*', like0) is not None:
                            like0 = re.sub(r'\^\.\*', '^.+', like0)
                    if re.search(r'%$', pd[1][1]) is not None:
                        like0 = like0 + '$'
                        if re.search(r'\.\*\$', like0) is not None:
                            like0 = re.sub(r'\.\*\$', '.+$', like0)
                    like1 = r'{}'.format(like0)
                    # print(like1)
                    for i in range(len(f_rd)):
                        if re.search(like1, f_rd[i][sf_zd[pd[1][0]]]) is not None:
                            f_rd[i][f_l] += 1

            if pd[2] == 1:
                flag += 1

    ans0 = []
    ans1 = []
    for i in range(len(f_rd)):
        if f_rd[i][f_l] >= flag:
            f_rd[i].pop(f_l)
            ans0.append(f_rd[i])
            ans1.append([])

    if zd['orderby'] is not None:
        paixu = zd['orderby']
        l_p = len(paixu)
        flag_p = 1
        if paixu[l_p - 1] in ['asc', 'ASC', 'desc', 'DESC']:
            if paixu[l_p - 1] in ['desc', 'DESC']:
                flag_p = 0
            paixu.pop(l_p - 1)
            l_p -= 1
        # print(paixu)
        # print(sf_zd)
        for i in range(l_p):
            paixu[i] = sf_zd[paixu[i]]
        # print(paixu)
        if flag_p == 1:
            PX.upsort(ans0, 0, len(ans0) - 1, paixu)
        else:
            PX.downsort(ans0, 0, len(ans0) - 1, paixu)

    chaxun0 = ans[0]
    for i in chaxun0:
        for j in range(len(ans0)):
            ans1[j].append(ans0[j][sf_zd[i]])
    ans += ans1
    return ans


# 多表查询？
def zuo_duo_chaxun(zd, db):
    ans = [[]]
    f_l = [], f_rd = [], sf_l = [], sf_rd = []
    sign = 0
    for i in zd['from']:
        res = rw.rd(i + '.dbf')
        f_l.append(res[0])
        f_rd.append(res[1])
        res = rw.rd(i + '_struct.dbf')
        sf_l.append(res[0])
        sf_rd.append(res[1])

    if zd['select'] != ['*']:
        ans = [zd['select']]
    else:
        sign = 1
        # for i in sf_rd:
        #     ans[0].append(i[0])

    sf_zd = {}  # 属性-下标字典
    sf_lx = []  # 属性类型
    b_len = 0
    for i in range(len(sf_rd)):
        for j in range(len(sf_rd[i])):
            sf_zd[sf_rd[i][j][0]] = b_len
            sf_zd[zd['from'][i] + '.' + sf_rd[i][j][0]] = b_len
            if sign == 1:
                ans[0].append(zd['from'][i] + '.' + sf_rd[i][j][0])
            sf_lx.append(sf_rd[i][j][1])
            b_len += 1

    b_len0 = 0
    for i in range(len(f_l)):
        for j in range(f_l[i]):
            if re.search(r'int', sf_lx[b_len0]) is not None:
                for k in range(len(f_rd[i])):
                    f_rd[i][k][j] = int(f_rd[i][k][j])
            elif re.search(r'float', sf_lx[b_len0]) is not None:
                for k in range(len(f_rd[i])):
                    f_rd[i][k][j] = float(f_rd[i][k][j])
            b_len0 += 1

    for i in range(len(f_rd)):  # 多表连接
        if i == 0:
            biao = f_rd[0].copy()
            biao0 = []
        else:
            b_h = len(biao)
            for j in range(b_h):
                for k in range(len(f_rd[i])):
                    biao0.append(biao[j] + f_rd[i][k])
            biao = biao0.copy()
            biao0 = []

    b_h = len(biao)
    for i in range(b_h):  # 遍历记录
        biao[i].append(0)

    flag = 0
    f_rd = biao
    f_l = b_h
    if zd['where'] is not None:
        panduan = zd['where']
        flag += 1
        for pd in panduan:
            if pd[0] == 0:  # 普通条件
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    pd[1][2] = int(pd[1][2])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    pd[1][2] = float(pd[1][2])

                if pd[1][1] == '=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '!=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '>':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] > pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '<':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] < pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '>=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] >= pd[1][2]:
                            f_rd[i][f_l] += 1
                elif pd[1][1] == '<=':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] <= pd[1][2]:
                            f_rd[i][f_l] += 1
            elif pd[0] == 1:  # 空值判断
                if pd[1][1] == 'is':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == '':
                            f_rd[i][f_l] += 1
                elif pd[1][1] == 'is not':
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] != '':
                            f_rd[i][f_l] += 1
            elif pd[0] == 2:  # in判断
                if re.search(r'int', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = int(pd[1][1][i])
                elif re.search(r'float', sf_lx[sf_zd[pd[1][0]]]) is not None:
                    for i in range(len(pd[1][1])):
                        pd[1][1][i] = float(pd[1][1][i])
                for i in range(len(f_rd)):
                    if f_rd[i][sf_zd[pd[1][0]]] in pd[1][1]:
                        f_rd[i][f_l] += 1
            elif pd[0] == 3:  # like判断
                if re.search(r'%', pd[1][1]) is None:
                    for i in range(len(f_rd)):
                        if f_rd[i][sf_zd[pd[1][0]]] == pd[1][1]:
                            f_rd[i][f_l] += 1
                else:
                    like0 = re.sub(r'%', '.*', pd[1][1])
                    if re.search(r'^%', pd[1][1]) is not None:
                        like0 = '^' + like0
                        if re.search(r'\^\.\*', like0) is not None:
                            like0 = re.sub(r'\^\.\*', '^.+', like0)
                    if re.search(r'%$', pd[1][1]) is not None:
                        like0 = like0 + '$'
                        if re.search(r'\.\*\$', like0) is not None:
                            like0 = re.sub(r'\.\*\$', '.+$', like0)
                    like1 = r'{}'.format(like0)
                    # print(like1)
                    for i in range(len(f_rd)):
                        if re.search(like1, f_rd[i][sf_zd[pd[1][0]]]) is not None:
                            f_rd[i][f_l] += 1

            if pd[2] == 1:
                flag += 1

    ans0 = []
    ans1 = []
    for i in range(len(f_rd)):
        if f_rd[i][f_l] >= flag:
            f_rd[i].pop(f_l)
            ans0.append(f_rd[i])
            ans1.append([])

    if zd['orderby'] is not None:
        paixu = zd['orderby']
        l_p = len(paixu)
        flag_p = 1
        if paixu[l_p - 1] in ['asc', 'ASC', 'desc', 'DESC']:
            if paixu[l_p - 1] in ['desc', 'DESC']:
                flag_p = 0
            paixu.pop(l_p - 1)
            l_p -= 1
        for i in range(l_p):
            paixu[i] = sf_zd[paixu[i]]
        if flag_p == 1:
            PX.upsort(ans0, 0, len(ans0) - 1, paixu)
        else:
            PX.downsort(ans0, 0, len(ans0) - 1, paixu)

    chaxun0 = ans[0]
    for i in chaxun0:
        for j in range(len(ans0)):
            ans1[j].append(ans0[j][sf_zd[i]])
    ans += ans1
    return ans


def al_gai(zd, db):
    file = db + '/' + zd['alter'][0] + '.dbf'
    structfile = db + '/' + zd['alter'][0] + '_struct.dbf'
    f_l, f_rd = rw.rd(file)
    sf_l, sf_rd = rw.rd(structfile)
    if zd['drop'] is not None:
        mf.DeleteStruct(zd['drop'], structfile, file)


    elif zd['add'] is not None:
        add0 = zd['add'].copy()
        if len(add0) == 2:
            add0.append('True')
            add0.append('False')
        elif len(add0) == 3:
            add0.append('False')
        print('structfile:', structfile)
        print('file:', file)
        print('add0:', add0)
        mf.AddStruct(structfile, file, add0[0], add0[1], add0[2], add0[3])
    elif zd['change'] is not None:
        for i in range(len(sf_rd)):
            if sf_rd[i][0] == zd['change'][0]:
                sf_rd[i][1] = zd['change'][1]
                break
        rw.w(structfile, "name C(25); type C(25); isNull C(5); isKey C(5)", sf_rd)

    elif zd['modify'] is not None:
        md0 = zd['modify'].copy()
        for i in range(len(sf_rd)):
            if sf_rd[i][0] == md0[0]:
                for j in range(len(md0)):
                    if j == 1:
                        if re.search(r'varchar', sf_rd[i][j]) is not None:
                            if re.search(r'varchar', md0[j]) is None:
                                return -1
                    sf_rd[i][j] = md0[j]
            break
        rw.w(structfile, "name C(25); type C(25); isNull C(5); isKey C(5)", sf_rd)
    elif zd['rename'] is not None:
        at.DeleteTable(zd['alter'][0], '')
        file = zd['rename'][0] + '.dbf'
        structfile = zd['rename'][0] + '_struct.dbf'
        rw.w(structfile, "name C(25); type C(25); isNull C(5); isKey C(5)", sf_rd)
        mf.UpDate(structfile, file, f_rd)
    return 0


def gongneng(sql, db):
    lx, gjz = se8.guanjianzi(sql)
    # print(se8.guanjianzi(sql))
    # return 0
    if lx == 3:
        li = [0, 0, 0, 0]
        from_flag = 0
        where_flag = 0
        if 'select' in gjz:
            li[0] = 1
        if 'from' in gjz:
            li[1] = 1
        if 'where' in gjz:
            li[2] = 1
            from_flag = 1
        if 'order by' in gjz:
            li[3] = 1
            where_flag = 1
        zd = c.cha(li, sql, from_flag, where_flag)
        # print(zd)
        if len(zd['from']) == 1:
            return chaxun(zd, db)
        else:
            return duo_chaxun(zd, db)
    elif lx == 2:
        if 'update' in gjz:
            li = [0, 0, 0]
            set_flag = 0
            li[0] = 1
            if 'set' in gjz:
                li[1] = 1
            if 'where' in gjz:
                li[2] = 1
                set_flag = 1
            xiugai(g.gai(li, sql, set_flag), db)
        elif 'alter table' in gjz:
            # print('gjz:', lx, gjz)
            li = [0, 0, 0, 0, 0, 0]
            if 'alter table' in gjz:
                li[0] = 1
            if 'drop column' in gjz:
                li[1] = 1
            if 'add column' in gjz:
                li[2] = 1
            if 'change column' in gjz:
                li[3] = 1
            if 'modify column' in gjz:
                li[4] = 1
            if 'rename to' in gjz:
                li[5] = 1
            # print(li)
            zd = al.gai_al(li, sql)
            return al_gai(zd, db)


# sql = 'select 属性1 from 测试 where 属性1 like "23"'
# zd = c.cha([1, 1, 1, 0], sql, 1, 0)
# print(zd)
#
# print(rw.rd('测试.dbf'))
# print(rw.rd('测试_struct.dbf'))
# print(chaxun(zd))

# print(rw.rd('test.dbf'))
# print(rw.rd('test_struct.dbf'))
# a = '123'
# b = int(a)
# c = float(a)
# print(b, type(b))
# print(c, type(c))

if __name__ == "__main__":
    # print(rw.rd('测试_struct.dbf'))
    # print(rw.rd('测试.dbf'))
    t = ' delete from test where name = `xiaoxiong`'
    # print(delete_sql(t))
    # print(delete0(delete_sql(t), "B"))
    # print(rw.rd('测试.dbf'))
