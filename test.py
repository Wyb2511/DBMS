import os

import yuyi
from ReadWrite import rd

'''
path = os.listdir(os.getcwd())
print(path)
print(os.getcwd())
for p in path:
    if os.path.isdir(p) and p != '.idea' and p != '__pycache__':
        print(p)
        L = os.listdir(p)
        print(L)
'''


# 修改格式
# python 读写文件
def find_all(data, s):
    r_list = []
    for r in range(len(data)):
        if data[r] == s:
            print(r)
            r_list.append(r)
    return r_list


def Standardization(sql_file):
    sql = open(sql_file, 'r', encoding='utf8')
    s = sql.read()
    print(s)
    pos = find_all(s, ',')
    k = 0
    str_list = list(s)
    for i in pos:
        k += 1
        i += k
    str_list.insert(i, '\n')
    s = ''.join(str_list)
    return s


# print(rd('B/website_struct.dbf'))
sql = 'use B; select * from test'
print(sql)
database = (sql.splitlines()[0].split()[1]).split(';')[0]
print(database)
print(yuyi.gongneng(sql, 'B'))
