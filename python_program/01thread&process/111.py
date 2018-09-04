import multiprocessing
import os

x = []
q = multiprocessing.Queue(5)

for i in range(6):
    if not q.full():
        q.put('消息%d'%i)
        print('添加消息%d'%i)

    else:
        print('消息队列已经满了')
print(q.qsize())


if q.empty():
    print('不空')
    for i in range(q.qsize()):

        print(q.get())
else:
    print('消息已经空了')