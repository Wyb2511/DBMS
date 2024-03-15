# 新建数据库
CREATE DATABASE C;

# 新建表
USE C;
CREATE TABLE User (
uid      INT(10)        NOT NULL,
wid      INT(10)        NOT NULL,
name    VARCHAR(20)    NOT NULL,
PRIMARY KEY (`uid`));

#插入数据
USE C;
INSERT INTO User (uid, wid, name) VALUES ('001','001', 'Wilson')

#修改数据
USE C;
UPDATE User SET uid = 002, wid = 003, name = "Tom"  where uid = 001

#删除数据
USE C;
DELETE FROM User  WHERE name = 'Tom'

#修改结构
USE C;
ALTER TABLE test DROP COLUMN age

#查询（多表连接）
USE B;
select uid, wid, User.name, 属性1, 属性2, website.name from User, 测试, website where User.name != 属性1 and uid < 2 order by uid, User.wid desc

#删除表
USE C;
DROP TABLE website

# 删除数据库
DROP DATABASE C;