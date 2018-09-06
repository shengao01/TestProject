# coding:utf-8
from generate_list import generate_list

tmp_list = generate_list()
print("before_sort:", tmp_list)

sort_list = []
while len(tmp_list) > 0:
    min_index = 0
    for i in range(0, len(tmp_list)):
        if tmp_list[min_index] > tmp_list[i]:
            min_index = i
    sort_list.append(tmp_list[min_index])
    tmp_list.pop(min_index)

    # print min_index
    # print tmp_list
print sort_list
