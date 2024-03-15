import re


def alter0(sql):
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE)\s+\S+\s+', sql)
    ans = re.sub(r'(alter\s+table|ALTER\s+TABLE)|\s+', '', ans.group())
    ans = re.split(r',', ans)
    return ans


def drop0(sql):
    ans = re.search(r'(drop\s+column|DROP\s+COLUMN).*', sql)
    ans = re.sub(r'(drop\s+column|DROP\s+COLUMN)\s+', '', ans.group())
    ans = re.split(r',\s*', ans)
    return ans


def add0(sql):
    ans = re.search(r'(add\s+column|ADD\s+COLUMN).*', sql)
    ans = re.sub(r'(add\s+column|ADD\s+COLUMN)\s+', '', ans.group())
    ans = re.split(r'\s+', ans)
    return ans


def change0(sql):
    ans = re.search(r'(change\s+column|CHANGE\s+COLUMN).*', sql)
    ans = re.sub(r'(change\s+column|CHANGE\s+COLUMN)\s+', '', ans.group())
    ans = re.split(r'\s+', ans)
    return ans


def modify0(sql):
    ans = re.search(r'(modify\s+column|MODIFY\s+COLUMN).*', sql)
    ans = re.sub(r'(modify\s+column|MODIFY\s+COLUMN)\s+', '', ans.group())
    ans = re.split(r'\s+', ans)
    return ans


def rename0(sql):
    ans = re.search(r'(rename\s+to|RENAME\s+TO).*', sql)
    ans = re.sub(r'(rename\s+to|RENAME\s+TO)\s+', '', ans.group())
    ans = re.split(r'\s+', ans)
    return ans


def gai_al(jiance, sql):
    ans = {'alter': None, 'drop': None, 'add': None, 'change': None, 'modify': None, 'rename': None}
    if jiance[0] == 1:
        ans['alter'] = alter0(sql)
    if jiance[1] == 1:
        ans['drop'] = drop0(sql)
    if jiance[2] == 1:
        ans['add'] = add0(sql)
    if jiance[3] == 1:
        ans['change'] = change0(sql)
    if jiance[4] == 1:
        ans['modify'] = modify0(sql)
    if jiance[5] == 1:
        ans['rename'] = rename0(sql)

    return ans



# print(add0('alter table XXX add column xx列名1,列属性'))
