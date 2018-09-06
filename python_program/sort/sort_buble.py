# coding:utf-8
from generate_list import generate_list

tmp_list = generate_list()
print("before_sort:", tmp_list)

k = len(tmp_list)-1
while k >= 0:
    for j in range(0, len(tmp_list)-1):
        if tmp_list[j] > tmp_list[j+1]:
            tmp_list[j], tmp_list[j+1] = tmp_list[j+1], tmp_list[j]
    k -= 1

print("after_sort:", tmp_list)
