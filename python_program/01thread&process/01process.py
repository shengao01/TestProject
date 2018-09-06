# coding = utf-8
import time
import multiprocessing
import os


def run():
    while True:
        time.sleep(0.8)
        print('that run', os.getpid())


process = multiprocessing.Process(target=run)
process.start()

if __name__ == '__main__':
    while True:
        time.sleep(1)
        print('this run', os.getpid())
    process.join()
