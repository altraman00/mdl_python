# -*- coding: UTF-8 -*-

from itertools import groupby

user_list = [
    {"uid": 1, "sex": "男", "age": 10},
    {"uid": 3, "sex": "男", "age": 20},
    {"uid": 4, "sex": "女", "age": 20},
    {"uid": 4, "sex": "女", "age": 20},
    {"uid": 2, "sex": "男", "age": 10}
]
# 多字段分组
user_sort = sorted(user_list, key=lambda x: (x["sex"], x["age"]))
# 多字段分组
user_group = groupby(user_sort, key=lambda x: (x["sex"], x["age"]))
for key, group in user_group:
    print(key, list(group))

sex_group = groupby(user_sort, key=lambda x: (x["sex"]))
for key, group in sex_group:
    print(key, list(group))

print("自定义分组key")


# 自定义分组key
def g(x):
    if (x['age'] > 0) and (x['age'] <= 10):
        return 'small'
    elif (x['age'] > 10) and (x['age'] <= 20):
        return 'mid'
    else:
        return 'max'


user_sort = sorted(user_list, key=lambda x: x["age"])
user_group = groupby(user_sort, key=g)
for key, group in user_group:
    print(key, list(group))
