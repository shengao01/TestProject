# coding:utf-8
from generate_list import generate_list

tmp_list = generate_list()
print("before_sort:", tmp_list)


for i in range(2, len(tmp_list)):
    for j in range(0, i):
        if tmp_list[j] > tmp_list[i]:
            tmp_list[j], tmp_list[i] = tmp_list[i], tmp_list[j]
print(tmp_list)
