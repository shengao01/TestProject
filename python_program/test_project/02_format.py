# coding:utf-8
name = (1, 2, 3)
adress = 'dfsdf'

a = "hahaha is %s %s" % (name, adress)

# 使用format的情况
b = "heihei is {}".format(name)
c = "heihei is {}{}{}".format(name, adress, name)

print(a)
print(b)
print(c)
