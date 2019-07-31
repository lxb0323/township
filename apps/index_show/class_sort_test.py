# import operator  #导入operator 包,pip install operator
 
# Departs = []#待排序列表
# class Department:#自定义的元素
#     def __init__(self,id,name,key,name1=''):
#         self.id = id
#         self.name = name
#         self.key = key
#         self.name1 = name1
 
# #创建元素和加入列表
# # Departs.append(Department(1, 'cbc' ,'1'))
# # Departs.append(Department(2, 'acd' ,'1'))
# # Departs.append(Department(3, 'bcd' ,'1'))
# # Departs.append(Department(1, 'bcd' ,'1'))
# # Departs.append(Department(2, 'acd' ,'3'))
# alist = []
# a = Department(id=1,name='c',key='1')
# a1 = Department(id=2,name='bc',key='2',name1=7)
# a2 = Department(id=3,name='ac',key='3')
# a3 = Department(id=4,name='dbc',key='4')
# Departs.append(a)
# Departs.append(a1)
# Departs.append(a2)
# Departs.append(a3)
# alist.append(a)
# alist.append(a1)
# alist.append(a2)
# alist.append(a3)
# print('\n'.join(['%s:%s' % item for item in Department.__dict__.items()]))
# print(getattr(a))
# from django.forms.models import model_to_dict

# data = self.get_queryset()

# for item in data:
#    item['product'] = model_to_dict(item['product'])

# return HttpResponse(json.simplejson.dumps(data), mimetype="application/json")

# getattr(Department)
# alist.sort(key=lambda x: x.name)
# print(alist,'-------11-----11-----')
# for n in alist:
#     n.pl = 3
#     print(str(n.id) + n.name + n.key + str(n.name1) + '--' + str(n.pl))
# #划重点#划重点#划重点----排序操作
# cmpfun = operator.attrgetter('name','id')#参数为排序依据的属性，可以有多个，这里优先id，使用时按需求改换参数即可
# Departs.sort(key=cmpfun, reverse=True)#使用时改变列表名即可
# #划重点#划重点#划重点----排序操作
 
# #此时Departs已经变成排好序的状态了，排序按照id优先，其次是name，遍历输出查看结果
# for depart in Departs:
#     print(str(depart.id) + depart.name + depart.key + str(depart.name1)) # + (1 if depart.args else depart.args)

# count = [{"name":'b','l':7},{"name":"a",'k':9}]

# def kl(lis):
#     x = []
#     for i in lis:
        
#         x.append(i['name'])
#     return x
# print(kl(count))
# # sorted(key=kl(count))
# # count.sort(key=lambda x: x['name'])
# print(count)

# d = [1,2,3,4]
# b = operator.itemgetter(1,0)
# print(b(d))
# for ai in d:
#     a = str(a)
# print


adict = {'a':1,'b':2,'c':3,'d':4}
new_d = list(adict.keys())
print(new_d)
bdict = {}
for i in new_d:
    if adict[i] >= 2:
        bdict[i] = adict[i]
print(bdict)
b= {'aa':11,'bb':22,'cc':33}
c = dict(b,**bdict)
print(c)