import random


# 冒泡排序
def sort(list):
    for i in range(len(list) - 1, 0, -1):
        for j in range(i):
            if list[j] < list[j + 1]:
                list[j], list[j + 1] = list[j + 1], list[j]
    return list


# 选择排序
def select_sort(list):
    n = len(list)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if list[j] < list[min_index]:
                min_index = j
        if min_index != i:
            list[min_index], list[i] = list[i], list[min_index]
    return list


# 插入排序
def insert_sort(list):
    for i in range(1, len(list)):
        for j in range(i, 0, -1):
            if list[j] < list[j - 1]:
                list[j], list[j - 1] = list[j - 1], list[j]
    return list


if __name__ == '__main__':
    list_1 = [random.randint(0, 1000) for i in range(10)]
    print(list_1)
    # list2 = sort(list_1)
    # print(list2)
    # list3 = select_sort(list_1)
    # print(list3)
    list4 = insert_sort(list_1)
    print(list4)
