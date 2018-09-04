# coding=utf-8
import time
from multiprocessing import Process, Queue


# 定义父进程的需要执行的任务 函数
def parent_mission(que):
    data = que.get()  # 从队列获取数据打印
    print(data)
    time.sleep(5)


# 定义子进程的需要执行的任务 函数
def children_mission(que):
    data = "hello"  # 输入hello就会被父进程拿到
    que.put(data)  # 往队列添加数据
    time.sleep(3)


def main():
    q = Queue()  # 在父进程中定义队列，实现与子进程通信
    p = Process(target=children_mission, args=(q,))
    p.start()  # 启动子进程 执行任务
    parent_mission(q)  # 在父进程中 执行任务
    p.join()


if __name__ == "__main__":
    main()
