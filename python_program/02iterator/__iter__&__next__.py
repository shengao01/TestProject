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
        # print(mylist.datas)
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
    mylist1 = Mylist()
    mylist1.add('asd')
    mylist1.add('asd123')
    mylist1.add('qwe')
    mylist1.add('qwe123')

    print([i for i in mylist1])
    # print([i for i in mylist1])
    # print([i for i in mylist1])
