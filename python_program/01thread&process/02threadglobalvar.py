import time
import multiprocessing
import os

num = 0


def run():
    global num
    time.sleep(1)
    num = 200


process = multiprocessing.Process(target=run)
process.start()


if __name__ == '__main__':

    num = 100

    process.join()
    print(num)
