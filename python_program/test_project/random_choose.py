# coding:utf-8
import random

def city(a):
    if a == 1:
        a = '大连'
    if a == 2:
        a = '成都'
    return a
list = []
b = 0
c = 0
for i in range(888888):
    a = random.randint(1, 2)
    a = city(a)
    if a == '大连':
        b += 1
    if a == '成都':
        c += 1

print b, c