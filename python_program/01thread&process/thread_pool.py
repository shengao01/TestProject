# 简单往队列中传输线程数
import threading
import time
import queue


class Threadingpool():
    def __init__(self, max_num=5):
        self.queue = queue.Queue(max_num)
        for i in range(max_num):
            self.queue.put(threading.Thread)

    def getthreading(self):
        return self.queue.get()

    def addthreading(self):
        self.queue.put(threading.Thread)


def func(p, i):
    time.sleep(1)
    print(i)
    p.addthreading()


if __name__ == "__main__":
    p = Threadingpool()
    # for i in range(30):
    for i in range(20, 30):
        thread = p.getthreading()
        t = thread(target=func, args=(p, i))
        t.start()
