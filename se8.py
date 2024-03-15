import re


def guanjianzi(input1):
    i=0
    a=[]
    b=[]
    # temp = input()
    # input1 = str(temp)

    #定义表
    ans = re.search(r'(create\s+table|CREATE\s+TABLE).*(INTO|into)',input1)
    if ans:
        a.extend([0])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['create table','into'])
        a.extend([b])
        return(a)
        i=1
    ans = re.search(r'(create\s+table|CREATE\s+TABLE).*(ON|on)',input1)
    if ans and i==0:
        a.extend([0])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['create table','on'])
        a.extend([b])
        return(a)
        i=1
    #编辑表字段    
    ans = re.search(r'(edit\s+table|EDIT\s+TABLE).*(IN|in)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['edit table','in'])
        a.extend([b])
        return(a)
        i=2
    else:
        if ans and i !=0:
            return('-1')
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(alter\s+column|ALTER\s+COLUMN)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','alter column'])
        a.extend([b])
        return(a)
        i=2
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(CHANGE\s+COLUMN|change\s+column)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','change column'])
        a.extend([b])
        return(a)
        i=2
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(MODIFY\s+COLUMN|modify\s+column)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','modify column'])
        a.extend([b])
        return(a)
        i=2     
    #更改表名    
    ans = re.search(r'(rename\s+table|RENAME\s+TABLE).*(IN|in)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['rename table','in'])
        a.extend([b])
        return(a)
        i=3
    else:
        if ans and i !=0:
            return('-1')
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(RENAME\s+TO|rename\s+to)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','rename to'])
        a.extend([b])
        return(a)
        i=3          
    #删除表        
    ans = re.search(r'(drop\s+table|DROP\s+TABLE).*(IN|in)',input1)
    if ans and i==0:
        a.extend([1])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['drop table','in'])
        a.extend([b])
        return(a)
        i=4
    else:
        if ans and i !=0:
            return('-1')
    #增加列，约束        
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(add\s+column|ADD\s+COLUMN)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','add column'])
        a.extend([b])
        return(a)
        i=5
    else:
        if ans and i !=0:
            return('-1')
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(add\s+constraint|ADD\s+CONSTRAINT)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','add constraint'])
        a.extend([b])
        return(a)
        i=5        
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(add|ADD)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','add'])
        a.extend([b])
        return(a)
        i=5        
    #插入数据        
    ans = re.search(r'(insert\s+into|INSERT\s+INTO).*(VALUES|values).*(IN|in)',input1)
    if ans and i==0:
        a.extend([0])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['insert into','values','in'])
        a.extend([b])
        return(a)
        i=6
    else:
        if ans and i !=0:
            return('-1')
    ans = re.search(r'(insert\s+into|INSERT\s+INTO).*(VALUES|values)',input1)
    if ans and i==0:
        a.extend([0])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['insert into','values'])
        a.extend([b])
        return(a)
        i=6        
    #删除数据        
    ans = re.search(r'(delete\s+from|DELETE\s+FROM).*(WHERE|where).*(IN|in)',input1)
    if ans and i==0:
        a.extend([1])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['delete from','where','in'])
        a.extend([b])
        return(a)
        i=7
    else:
        if ans and i !=0:
            return('-1')
    ans = re.search(r'(delete\s+from|DELETE\s+FROM).*(WHERE|where)',input1)
    if ans and i==0:
        a.extend([1])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['delete from','where'])
        a.extend([b])
        return(a)
        i=7
    #修改数据    
    ans = re.search(r'(update|UPDATE).*(set|SET).*(where|WHERE).*(IN|in)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['update','set','where','in'])
        a.extend([b])
        return(a)
        i=8
    else:
        if ans and i !=0:
            return('-1')
    ans = re.search(r'(update|UPDATE).*(set|SET).*(where|WHERE)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['update','set','where'])
        a.extend([b])
        return(a)
        i=8
    #查询    
    ans = re.search(r'(select|SELECT).*(from|FROM)',input1)
    if ans and i==0:
        a.extend([3])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['select','from'])
        i=9
        ans = re.search(r'(left\s+join|LEFT\s+JOIN)',input1)
        if ans:
            b.extend(['left join'])
        ans = re.search(r'(right\s+join|RIGHT\s+JOIN)',input1)
        if ans:
            b.extend(['right join'])
        ans = re.search(r'(cross\s+join|CROSS\s+JOIN)',input1)
        if ans:
            b.extend(['cross join'])
        ans = re.search(r'(full\s+join|FULL\s+JOIN)',input1)
        if ans:
            b.extend(['full join'])    
        ans = re.search(r'(where|WHERE)',input1)
        if ans:
            b.extend(['where']) 
        ans = re.search(r'(group\s+by|GROUP\s+BY)',input1)
        if ans:
            b.extend(['group by']) 
        ans = re.search(r'(having|HAVING)',input1)
        if ans:
            b.extend(['having']) 
        ans = re.search(r'(order\s+by|ORDER\s+BY)',input1)
        if ans:
            b.extend(['order by'])
        a.extend([b])
        return(a)        
    else:
        if ans and i !=0:
            return('-1')
        #删除列，约束
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(drop\s+column|DROP\s+COLUMN)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','drop column'])
        a.extend([b])
        return(a)
        i=10
    else:
        if ans and i !=0:
            return('-1')
    ans = re.search(r'(alter\s+table|ALTER\s+TABLE).*(drop|DROP)',input1)
    if ans and i==0:
        a.extend([2])
        ans = re.search(r'(use|USE)',input1)
        if ans:
            b.extend(['use'])
        b.extend(['alter table','drop'])
        a.extend([b])
        return(a)
        i=10

    
    if i==0:
        return('-2')    
    i=0    

    

       
# print(guanjianzi('select a.*, ad.* from test_a left join test_a_description on a.id=ad.parent_id;'))

    

