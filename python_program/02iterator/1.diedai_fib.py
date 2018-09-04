# 创建一个斐波那契数列迭代器

class FibIterator(object):
    def __init__(self, n):
        self.n = n
        self.pos = 0
        self.num1 = 0
        self.num2 = 1

    def __next__(self):
        if self.pos < self.n:
            num = self.num1
            self.num1, self.num2 = self.num2, self.num1+self.num2
            self.pos += 1
            return num
        else:
            raise StopIteration

    def __iter__(self):
        return self


if __name__ == '__main__':
    fib = FibIterator(30)
    for num in fib:
        print(num)
    b = list(fib)
    a = list(FibIterator(10))
    print(b)
    print(a)

    b = tuple(fib)
    print(b)


def fib(n):
    pos = 0
    num0 = 0
    num1 = 1
    while pos < n:
        yield num0
        num0, num1 = num1, num0 + num1
        pos += 1
    else:
        return ""


f = fib(10)
for i in range(10):
    print(next(f))
