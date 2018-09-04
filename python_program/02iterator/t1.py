class MyIterator(object):
    def __init__(self, n):
        self.n = n
        self.pos = 0
        self.pre = 0
        self.cur = 1

    def __next__(self):
        if self.pos<self.n:
            num = self.pre
            self.pre, self.cur = self.cur, self.cur+self.pre
            self.pos+=1
            return num

        else:
            raise StopIteration

    def __iter__(self):
        return self

if __name__ == '__main__':
    gen = (i for i in MyIterator(10))
    print(sum(gen))
    for i in gen:
        print(i)
    print(list(MyIterator(10)))
