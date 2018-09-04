import time
import threading

def work1():
    while True:
        print('-----this is work1-----')
        yield
        time.sleep(1)


def work2():
    while True:
        print('-----this is work2-----')
        yield
        time.sleep(1)


def main():
    w1 = work1()
    w2 = work2()
    while True:
        next(w1)
        next(w2)


if __name__ == '__main__':
    main()
