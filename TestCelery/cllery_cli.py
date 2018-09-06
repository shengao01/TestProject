# coding:utf-8
from task_test import my_task1

res = my_task1.delay(3, 4)
# res.ready()
res.get()
