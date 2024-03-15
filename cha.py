import re


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
def use0(sql):
    ans = re.search(r'(use|USE).*(select|SELECT)\s+', sql)
    # print(ans.group())
    ans = [re.sub(r'use|USE|select|SELECT|\s', '', ans.group())]
    # print(ans)
    return ans


def select0(sql):
    ans = re.search(r'(select|SELECT).*(from|FROM)\s+', sql)
    # print(ans.group())
    ans = re.sub(r'select|SELECT|from|FROM|\s', '', ans.group())
    # print(ans)
    ans = re.split(r',', ans)
    # print(ans)
    return ans


def from0(sql, flag):
    if flag == 0:
        ans = re.search(r'(from|FROM).*', sql)
    else:
        ans = re.search(r'(from|FROM).*(where|WHERE)\s+', sql)
    # print(ans.group())
    ans = re.sub(r'from|FROM|where|WHERE|\s', '', ans.group())
    # print(ans)
    ans = re.split(r',', ans)
    # print(ans)
    return ans


def from1(sql):
    ans = re.search(r'(from|FROM).*(on|ON)\s+', sql)
    # print(ans.group())
    ans = re.sub(r',\s*', ',', ans.group())
    # print(ans)
    ans = re.sub(r'(from|FROM)\s+|(left\s+join|LEFT\s+JOIN|right\s+join|RIGHT\s+JOIN)\s+|\s+(on|ON)\s+', '', ans)
    # print(ans)
    ans = re.split(r',|\s+', ans)
    # print(ans)
    return ans

# print(from1('select a.*, ad.* from test_a left join test_a_description, aaa, bbb on a.id=ad.parent_id;'))


def on0(sql):
    ans = re.search(r'\s+(on|ON)\s+.*', sql)
    # print(ans.group())
    ans = re.sub(r'\s+(on|ON)\s+', '', ans.group())
    # print(ans)
    ans = re.sub(r'\s', '', ans)
    # print(ans)
    ans0 = [0, 1, 2]
    if re.search(r'!=|<>', ans) is not None:
        ans0[1] = '!='
    elif re.search(r'>=', ans) is not None:
        ans0[1] = '>='
    elif re.search(r'<=', ans) is not None:
        ans0[1] = '<='
    elif re.search(r'=', ans) is not None:
        ans0[1] = '='
    elif re.search(r'>', ans) is not None:
        ans0[1] = '>'
    elif re.search(r'<', ans) is not None:
        ans0[1] = '<'
    li1 = re.split(r'!=|<>|>=|<=|=|>|<', ans)
    # print(li1)
    ans0[0] = li1[0]
    ans0[2] = re.sub(r'\'|\"', '', li1[1])
    return ans0

# print(on0('select a.*, ad.* from test_a left join test_a_description, aaa, bbb on a.id=ad.parent_id;'))


def where0(sql, flag):
    li = []
    li0 = []
    if flag == 0:
        ans = re.search(r'(where|WHERE).*', sql)
    else:
        ans = re.search(r'(where|WHERE).*(order\s+by|ORDER\s+BY)', sql)
    # print(ans.group())
    ans = re.sub(r'where|WHERE|order\s+by|ORDER\s+BY|', '', ans.group())
    # print(ans)
    zj = re.findall(r'and|AND|or|OR', ans)
    l0 = len(zj)
    # print(zj)
    ans = re.split(r'and|AND|or|OR', ans)
    l1 = len(ans)
    # print(ans)
    for i in range(l1):
        li0 = []
        if re.search(r'\s+is\s+null\s*|\s+IS\s+NULL\s*|\s+is\s+not\s+null\s*|\s+IS\s+NOT\s+NULL\s*', ans[i]) is not None:  # 空值判断
            li0.append(1)
            if re.search(r'\s+is\s+not\s+null\s*|\s+IS\s+NOT\s+NULL\s*', ans[i]) is not None:
                ans0 = re.sub(r'\s+is\s+not\s+null\s*|\s+IS\s+NOT\s+NULL\s*|\s', '', ans[i])
                li0.append([ans0, 'is not'])
            else:
                ans0 = re.sub(r'\s+is\s+null\s*|\s+IS\s+NULL\s*|\s', '', ans[i])
                li0.append([ans0, 'is'])
                # print(li0)
        elif re.search(r'\s+in\s+|\s+IN\s+', ans[i]):  # in判断
            li0.append(2)
            ans0 = re.split(r'\s+in\s+|\s+IN\s+', ans[i])
            # print(ans0)
            ans0[0] = re.sub(r'\s', '', ans0[0])
            ans0[1] = re.sub(r'\(|\)|\s|\'|\"', '', ans0[1])
            # print(ans0)
            ans0[1] = re.split(r',', ans0[1])
            li0.append(ans0)
            # print(li0)
        elif re.search(r'\s+like\s+|\s+LIKE\s+', ans[i]):  # like判断
            li0.append(3)
            ans0 = re.split(r'\s+like\s+|\s+LIKE\s+', ans[i])
            ans0[0] = re.sub(r'\s', '', ans0[0])
            ans0[1] = re.sub(r'\s*\'\s*|\s*\"\s*', '', ans0[1])
            li0.append(ans0)
            # print(li0)
        else:  # 普通判断
            li0.append(0)
            ans0 = [0, 1, 2]
            ans[i] = re.sub(r'\s', '', ans[i])
            print(ans[i])
            if re.search(r'!=|<>', ans[i]) is not None:
                ans0[1] = '!='
            elif re.search(r'>=', ans[i]) is not None:
                ans0[1] = '>='
            elif re.search(r'<=', ans[i]) is not None:
                ans0[1] = '<='
            elif re.search(r'=', ans[i]) is not None:
                ans0[1] = '='
            elif re.search(r'>', ans[i]) is not None:
                ans0[1] = '>'
            elif re.search(r'<', ans[i]) is not None:
                ans0[1] = '<'
            li1 = re.split(r'!=|<>|>=|<=|=|>|<', ans[i])
            # print(li1)
            ans0[0] = li1[0]
            ans0[2] = re.sub(r'\'|\"', '', li1[1])
            li0.append(ans0)
            # print(li0)
        if i == l0:
            li0.append(0)
        else:
            if zj[i] == 'and':
                li0.append(1)
            else:
                li0.append(2)
        li.append(li0)
        # print(li0)
    # print(li)
    return li


def where1(sql, flag):
    li = []
    li0 = []
    if flag == 0:
        ans = re.search(r'(where|WHERE).*', sql)
    else:
        ans = re.search(r'(where|WHERE).*(order\s+by|ORDER\s+BY)', sql)
    # print(ans.group())
    ans = re.sub(r'where|WHERE|order\s+by|ORDER\s+BY|', '', ans.group())
    # print(ans)
    zj = re.findall(r'and|AND|or|OR', ans)
    l0 = len(zj)
    # print(zj)
    ans = re.split(r'and|AND|or|OR', ans)
    l1 = len(ans)
    # print(ans)
    for i in range(l1):
        li0 = []
        if re.search(r'\s+is\s+null\s+|\s+IS\s+NULL\s+|\s+is\s+not\s+null\s+|\s+IS\s+NOT\s+NULL\s+', ans[i]) is not None:  # 空值判断
            li0.append(1)
            if re.search(r'\s+is\s+not\s+null\s+|\s+IS\s+NOT\s+NULL\s+', ans[i]) is not None:
                ans0 = re.sub(r'\s+is\s+not\s+null\s+|\s+IS\s+NOT\s+NULL\s+|\s', '', ans[i])
                if re.search(r'\.', ans0) is not None:
                    ans0 = re.split(r'\.', ans0)
                li0.append([ans0, 'is not'])
            else:
                ans0 = re.sub(r'\s+is\s+null\s+|\s+IS\s+NULL\s+|\s', '', ans[i])
                if re.search(r'\.', ans0) is not None:
                    ans0 = re.split(r'\.', ans0)
                li0.append([ans0, 'is'])
                # print(li0)
        elif re.search(r'\s+in\s+|\s+IN\s+', ans[i]):  # in判断
            li0.append(2)
            ans0 = re.split(r'\s+in\s+|\s+IN\s+', ans[i])
            # print(ans0)
            ans0[0] = re.sub(r'\s', '', ans0[0])
            if re.search(r'\.', ans0[0]) is not None:
                ans0[0] = re.split(r'\.', ans0[0])
            ans0[1] = re.sub(r'\(|\)|\s|\'|\"', '', ans0[1])
            # print(ans0)
            ans0[1] = re.split(r',', ans0[1])
            li0.append(ans0)
            # print(li0)
        elif re.search(r'\s+like\s+|\s+LIKE\s+', ans[i]):  # like判断
            li0.append(3)
            ans0 = re.split(r'\s+like\s+|\s+LIKE\s+', ans[i])
            ans0[0] = re.sub(r'\s', '', ans0[0])
            if re.search(r'\.', ans0[0]) is not None:
                ans0[0] = re.split(r'\.', ans0[0])
            ans0[1] = re.sub(r'\s*\'\s*|\s*\"\s*', '', ans0[1])
            li0.append(ans0)
            # print(li0)
        else:  # 普通判断
            li0.append(0)
            ans0 = [0, 1, 2]
            ans[i] = re.sub(r'\s', '', ans[i])
            if re.search(r'!=|<>', ans[i]) is not None:
                ans0[1] = '!='
            elif re.search(r'>=', ans[i]) is not None:
                ans0[1] = '>='
            elif re.search(r'<=', ans[i]) is not None:
                ans0[1] = '<='
            elif re.search(r'=', ans[i]) is not None:
                ans0[1] = '='
            elif re.search(r'>', ans[i]) is not None:
                ans0[1] = '>'
            elif re.search(r'<', ans[i]) is not None:
                ans0[1] = '<'
            li1 = re.split(r'!=|<>|>=|<=|=|>|<', ans[i])
            # print(li1)
            if re.search(r'\.', li1[0]) is not None:
                li1[0] = re.split(r'\.', li1[0])
            ans0[0] = li1[0]
            ans0[2] = re.sub(r'\'|\"', '', li1[1])
            li0.append(ans0)
            # print(li0)
        if i == l0:
            li0.append(0)
        else:
            if zj[i] == 'and':
                li0.append(1)
            else:
                li0.append(2)
        li.append(li0)
        # print(li0)
    # print(li)
    return li


def orderby0(sql):
    ans = re.search(r'order\s+by.*|ORDER\s+BY.*', sql)
    ans = re.sub(r'\s*,\s*', ',', ans.group())
    # print(ans.group())
    ans = re.sub(r'order\s+by\s+|ORDER\s+BY\s+', '', ans)
    # print(ans)
    ans = re.split(r',|\s+', ans)
    # print(ans)
    return ans


def orderby1(sql):
    ans = re.search(r'order\s+by.*|ORDER\s+BY.*', sql)
    # print(ans.group())
    ans = re.sub(r'\s*,\s*', ',', ans.group())
    ans = re.sub(r'order\s+by\s+|ORDER\s+BY\s+|', '', ans)
    # print(ans)
    ans = re.split(r',|\s+', ans)
    # print(ans)

    for i in range(len(ans)):
        if re.search(r'\.', ans[i]) is not None:
            ans[i] = re.split(r'\.', ans[i])
    # print(ans)
    return ans


def cha(jiance, sql, from_flag, where_flag):
    ans = {'select': None, 'from': None, 'where': None, 'orderby': None}
    if jiance[0] == 1:
        ans['select'] = select0(sql)
    if jiance[1] == 1:
        ans['from'] = from0(sql, from_flag)
    if jiance[2] == 1:
        ans['where'] = where0(sql, where_flag)
    if jiance[3] == 1:
        ans['orderby'] = orderby0(sql)
    # print(ans)
    return ans


if __name__ == '__main__':
    sql = 'select id1, id2 from table1, table2 where table1.id0 = 0 and table2.id1 is null or table1.id2 in (100,200) and table1.id3 like "%zz%" order by id0, table1.id1 asc'
    # print(sql)
    # from0(sql, 1)
    # where1(sql, 1)
    # orderby1(sql)
    # select0(sql)
    # from0(sql, 1)
    # where0(sql, 1)
    # orderby0(sql)
# print(use0('use test select id, name from table1 where id = 0 and name = "zzz" or id1 = 2'))
# select0('use test select id, name from table1 where id = 0 and name = "zzz" or id1 = 2')


# if re.search(r'\)\s+(value|VALUE)', sql) is None:
#     pass
# else:
#     ans = re.search(r'insert\s+into.*\(')
#     ans = re.sub(r'insert\s+into.*\(', '', ans.group())
