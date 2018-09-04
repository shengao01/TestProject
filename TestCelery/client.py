# coding:utf-8
import time
from proj.tasks import add, mul

res_add = add.apply_async((2, 3))
res_mul = mul.apply_async((4, 5))

print(res_add)
print(res_mul)
print(res_mul.ready())
print(res_mul.ready())

# time.sleep(3)

# print(res_add.get())
# print(res_mul.get())
