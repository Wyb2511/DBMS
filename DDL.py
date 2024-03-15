import re
from AboutTable import CreateTable, DeleteTable
from AboutDatabase import NewDatabase, DeleteDatabase
from ReadWrite import rd
import re

import numpy as np

import se8
from ReadWrite import w, rd, Type

from Modification import AddData

sqlf = 'SQL.sql'


def DDLCreateDatabase(sql):
    database = (sql.splitlines()[0].split()[2]).split(';')[0]
    NewDatabase(database)


def DDLDropDatabase(sql):
    database = (sql.splitlines()[0].split()[2]).split(';')[0]
    DeleteDatabase(database)


def DDLCreateTable(sql):
    structs = []
    # sql = open(sql_file, 'r', encoding='utf8')
    LIST = sql.splitlines()
    i = 0
    pk = []
    database = (sql.splitlines()[0].split()[1]).split(';')[0]
    print(database)
    table = ''
    # print("数据库名称:", database)
    for item in LIST:
        if i == 1:
            table = item.split()[2]
        if 'PRIMARY' in item:
            r = r'`(.*?)`'
            pk += re.findall(r, item)
        if item == '\n' or item == ');':
            LIST.remove(item)
        if i >= 2 and item.split()[0] != 'PRIMARY' and item.split()[0] != 'CONSTRAIN':
            line = item.split()
            line[1] = line[1].lower()
            if line[2] == 'NOT':
                del line[2]
                del line[2]
                line.append('True')  # 占位
            structs.append(line)
        i += 1
    for struct in structs:
        if struct[0] in pk:
            struct.append('True')
        else:
            struct.append('False')
    CreateTable(table, structs, database)


def DDLDropTable(sql):
    # sql = open(sql_file, 'r', encoding='utf8')
    LIST = sql.splitlines()
    database = re.sub(r'use|USE|\s', '', re.search(r'(use|USE).*', LIST[0]).group())
    table = LIST[1].split()[2]
    DeleteTable(table, database)


if __name__ == '__main__':
    # DDLCreateTable(sqlf)
    # rd('B/website_struct.dbf')
    # print(rd('测试_struct.dbf'))
    # print(rd('测试.dbf'))
    t1 = 'INSERT INTO website (id,name) VALUES (`009`,`Wilson`)'
    print(insert0(insert_sql(t1), "B"))
    # print(rd('测试.dbf'))
    # INSERT INTO 测试(属性1,属性2) VALUES ('Gates', 'Bill')
    # INSERT INTO 测试(属性1) VALUES ('Gates')

    # print(rd('测试_struct.dbf'))
