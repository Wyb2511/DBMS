import re
import cha as c  # c代表查
import gai as g  # g代表改
import ReadWrite as rw
import paixu as PX
import se8
import Modification as mf
import Alter as al
import AboutTable as at

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
def chaxun(zd):
    ans = [[]]
    file = zd['from'][0]+'.dbf'
    structfile = zd['from'][0]+'_struct.dbf'
    f_l, f_rd = rw.rd(file)
    sf_l, sf_rd = rw.rd(structfile)
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
                    like1 = r'{}'. format(like0)
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
        if paixu[l_p-1] in ['asc', 'ASC', 'desc', 'DESC']:
            if paixu[l_p - 1] in ['desc', 'DESC']:
                flag_p = 0
            paixu.pop(l_p-1)
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


def xiugai(zd):
    file = zd['update'][0] + '.dbf'
    structfile = zd['update'][0] + '_struct.dbf'
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


def duo_chaxun(zd):
    ans = [[]]
    f_l = []
    f_rd = []
    sf_l = []
    sf_rd = []
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
                    like1 = r'{}'. format(like0)
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
        if paixu[l_p-1] in ['asc', 'ASC', 'desc', 'DESC']:
            if paixu[l_p - 1] in ['desc', 'DESC']:
                flag_p = 0
            paixu.pop(l_p-1)
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


def zuo_duo_chaxun(zd):
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
                    like1 = r'{}'. format(like0)
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
        if paixu[l_p-1] in ['asc', 'ASC', 'desc', 'DESC']:
            if paixu[l_p - 1] in ['desc', 'DESC']:
                flag_p = 0
            paixu.pop(l_p-1)
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


def al_gai(zd):
    file = zd['alter'][0] + '.dbf'
    structfile = zd['alter'][0] + '_struct.dbf'
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


def gongneng(sql):
    lx, gjz = se8.guanjianzi(sql)
    # print(se8.guanjianzi(sql))
    # return 0
    # print('gjz:',lx, gjz)
    # print('alter table' in gjz)
    if lx == 3:
        if 'select' in gjz:
            li = [0, 0, 0, 0]
            from_flag = 0
            where_flag = 0
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
                return chaxun(zd)
            else:
                return duo_chaxun(zd)
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
            xiugai(g.gai(li, sql, set_flag))
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
            return al_gai(zd)




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

