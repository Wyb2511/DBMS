import re
import cha


def update0(sql):
    ans = re.search(r'(update|UPDATE).*(set|SET)\s+', sql)
    # print(ans.group())
    ans = [re.sub(r'update|UPDATE|set|SET|\s', '', ans.group())]
    # print(ans)
    return ans


def set0(sql, flag):
    li0 = []
    if flag == 0:
        ans = re.search(r'(set|SET).*', sql)
    else:
        ans = re.search(r'(set|SET).*(where|WHERE)', sql)
    # print(ans.group())
    ans = re.sub(r'set|SET|where|WHERE|\s', '', ans.group())
    ans = re.split(r',', ans)
    l0 = len(ans)
    for i in range(l0):
        ans0 = [0, 1, 2]
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
        ans[i] = re.sub(r'\'|\"', '', ans[i])
        li1 = re.split(r'!=|<>|>=|<=|=|>|<', ans[i])
        # print(li1)
        # print(li1)
        ans0[0] = li1[0]
        ans0[2] = li1[1]
        li0.append(ans0)
    # print(li0)
    return li0


def where0(sql):
    return cha.where0(sql, 0)


def gai(jiance, sql, set_flag):
    ans = {'update': None, 'set': None, 'where': None}
    if jiance[0] == 1:
        ans['update'] = update0(sql)
    if jiance[1] == 1:
        ans['set'] = set0(sql, set_flag)
    if jiance[2] == 1:
        ans['where'] = where0(sql)

    return ans


if __name__ == '__main__':
    sql = 'update test set id0 = 0, id1 = 1, id2 = 3 where id0 = 0 and id1 is null or id2 in (100,200) and id3 like "%zz%" '
    print(sql)
    print(gai([1, 1, 1], sql, 1))

