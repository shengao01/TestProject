# coding:utf-8
import random


def generate_list(a=10, b=100):
    tmp_list = []
    for i in range(a):
        item = random.randint(0, b)
        tmp_list.append(item)
    return tmp_list
