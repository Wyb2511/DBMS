import dbf

# 创建test.dbf文件 共两列 name 字符串 长度25；age 数值 长度3
table = dbf.Table(filename='B/test.dbf', field_specs='name C(25); age C(25)', codepage='cp936')
# 修改为读写模式
table.open(mode=dbf.READ_WRITE)
# 添加数据
table.append(('xiaoxiong', '18'))
table.append(('xiao', '18'))
table.append(('xiong', '18'))
print(table[1])
table.close()
table = dbf.Table(filename='B/test_struct.dbf', field_specs='name C(25);type C(25);notNull C(5);isKey C(5)', codepage='cp936')
# 修改为读写模式
table.open(mode=dbf.READ_WRITE)
# 添加数据
table.append(('name', 'varchar(25)', 'False', 'True'))
table.append(('age', 'int(10)', 'True', 'False'))
print(table[1])
table.close()
