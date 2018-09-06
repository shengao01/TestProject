# def singleton(fun):
#     instances = {}
#
#     def _singleton():
#         if fun not in instances:
#             instances[fun] = fun()
#         return instances[fun]
#
#     return _singleton
#
#
# @singleton
# class MyClass(object):
#     a = 1
#
#     def __init__(self, x=0):
#         self.x = x
#
# one = MyClass()
# two = MyClass()
#
# one.a = 3
# print(one.a)
# print(two.a)


def singleton(cls, *args, **kw):
    instance = {}

    def _singleton():
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]

    return _singleton


@singleton
class test_singleton(object):
    num_sum = 1
    def __init__(self):
        self.num_sum = 0

    def add(self):
        self.num_sum += 100


a = test_singleton()
b = test_singleton()

a.num = 3

# a = a.add()
# b = b.add()
print(a.num_sum)
print(b.num_sum)
a.add()
print(a.num_sum)
a.add()
print(b.num_sum)
print(b.num)
print(a)
print(b)
