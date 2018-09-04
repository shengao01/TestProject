# coding:utf-8
from celery import group

from proj.tasks import my_task1
from proj.tasks import my_task2
from proj.tasks import my_task3

# 将多个signature放入同一组中
my_group = group((my_task1.s(10, 10), my_task2.s(20, 20), my_task3.s(30, 10)))
ret = my_group()  # 执行组任务
# print(ret.get())  # 输出每个任务结果
print(ret)  # 输出每个任务结果