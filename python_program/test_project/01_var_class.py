class Person():
    # name = []
    name = 'aaa'

p1 = Person()
p2 = Person()

print(p2.name)

Person.name = 'ccc'
# p1.name.append('1')
p1.name = 'bbb'

print(p1.name)
print(p2.name)
print(Person.name)

