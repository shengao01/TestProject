
print('----3.初始化用户列表----')
users = []
# 创建用户
class User(object):
    def __init__(self,name,uuid,ip):
        self.name = name
        self.uuid = uuid
        self.ip = ip

def addUser(name,uuid,ip):
    user = User(name,uuid,ip)
    users.append(user)

def removeUser(name,uuid,ip):
    user = User(name, uuid, ip)
    users.remove(user)

def changeName(uuid,name):
    for user in users:
        if user.uuid == uuid:
            user.name = name
            break


def outputUserList():
    if len(users) == 0:
        print('no users')
        return

    for user in users:
        print('  user: %s %s %s'%(user.name, user.uuid, user.ip))
