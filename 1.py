import yuyi
import ReadWrite as rw
from DML import *

# sql = 'select * from User'
# print(sql)
# print(yuyi.gongneng(sql))
# sql1 = 'update User set uid = 0, wid = 9, name = "20"  where uid = 0'
# print(sql1)
# yuyi.gongneng(sql1)
# print(yuyi.gongneng(sql))

# sql2 = 'select uid, wid, User.name, 属性1, 属性2, website.name from User, 测试, website where User.name != 属性1 and uid < 2 order by uid, User.wid desc'
# sql2 = 'select * from User, 测试, website where User.name != 属性1 and uid < 2 order by uid, User.wid desc'
# print(sql2)
# print(yuyi.gongneng(sql2))
# print("???")
# print(rw.rd('User_struct.dbf'))
# print(rw.rd('User.dbf'))
#
sql3 = 'ALTER TABLE test drop column age'
print(gongneng(sql3, 'B'))
#
# print(rw.rd('User_struct.dbf'))
print(rw.rd('B/test.dbf'))
