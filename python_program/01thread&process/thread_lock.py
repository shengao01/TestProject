# coding:utf-8
import threading
import time

g_num = 0

def test1(num):
    global g_num
    for i in range(num):
        # True表示堵塞 即如果这个锁在上锁之前已经被上锁了，那么这个线程会在这里一直等待到解锁为止
        # False表示非堵塞，即不管本次调用能够成功上锁，都不会卡在这,而是继续执行下面的代码
        mutexFlag = mutex.acquire(True)
        if mutexFlag:  # 如果上锁成功
            g_num += 1
            mutex.release()  # 解锁

    print("---test1---g_num=%d" % g_num)


def test2(num):
    global g_num
    for i in range(num):
        mutexFlag = mutex.acquire(True)  # True表示堵塞
        if mutexFlag:
            g_num += 1
            mutex.release()

    print("---test2---g_num=%d" % g_num)


# 创建一个互斥锁
# 这个所默认是未上锁的状态
mutex = threading.Lock()

p2 = threading.Thread(target=test2, args=(1000000,))
p2.start()

p1 = threading.Thread(target=test1, args=(1000000,))
p1.start()


while len(threading.enumerate()) != 1:
    time.sleep(1)

print("2个线程对同一个全局变量操作之后的最终结果是:%s" % g_num)
