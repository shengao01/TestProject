class Mylist(object):
    def __init__(self):
        self.datas = []

    def add(self, a):
        self.datas.append(a)

    def __iter__(self):
        myiter = MyIterator(self)
        return myiter


class MyIterator(object):
    def __init__(self, mylist):
        self.mylist = mylist
        self.pos = 0

    def __next__(self):
        if len(self.mylist.datas) > self.pos:
            data = self.mylist.datas[self.pos]
            self.pos += 1
            return data
        else:
            raise StopIteration

    def __iter__(self):
        return self

if __name__ == '__main__':
    mylist = Mylist()
    mylist.add('asd')
    mylist.add('asd123')
    mylist.add('qwe')
    mylist.add('qwe123')

    for i in mylist:
        print(i)
