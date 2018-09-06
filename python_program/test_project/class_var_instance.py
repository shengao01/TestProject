class Test():
    num_instance = 0
    def __init__(self,name):
        self.name = name
        self.num_instance += 1
        # Test.num_instance += 1

a = Test('Jack')
print(Test.num_instance)
print(a.num_instance)

a = Test('Lucy')
print(Test.num_instance)
print(a.num_instance)

a = Test('Jack')
print(Test.num_instance)
print(a.num_instance)

b = Test('Lucy')
print(Test.num_instance)
print(b.num_instance)



