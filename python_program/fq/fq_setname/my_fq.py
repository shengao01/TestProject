# coding=utf-8
# 框架搭建
from socket import *
import uuid
import os
import getpass
import threading
import feiqcore
import feiqnet
import feiquser


def handleNetwork(recvPack, ip):
    if recvPack[feiqcore.cmd] == feiqcore.online:
        if recvPack[feiqcore.uuid] == feiqnet.uuid:
            return True
        feiquser.addUser(recvPack[feiqcore.name], recvPack[feiqcore.uuid], ip)
        # 回应我也在线
        feiqnet.onlineack(ip)
        print('  user: %s %s %s online' % (recvPack[feiqcore.name], recvPack[feiqcore.uuid], ip))

    elif recvPack[feiqcore.cmd] == feiqcore.onlineack:
        feiquser.addUser(recvPack[feiqcore.name], recvPack[feiqcore.uuid], ip)

    elif recvPack[feiqcore.cmd] == feiqcore.offline:
        if recvPack[feiqcore.uuid] == feiqnet.uuid:
            return False
        feiquser.removeUser(recvPack[feiqcore.name], recvPack[feiqcore.uuid], ip)

    elif recvPack[feiqcore.cmd] == feiqcore.msg:
        if recvPack[feiqcore.uuid] == feiqnet.uuid:
            return True

        msg = recvPack[feiqcore.msg]
        print(("%s(%s)say:%s") % (recvPack[feiqcore.name], ip, msg))

    elif recvPack[feiqcore.cmd] == feiqcore.setname:
        if recvPack[feiqcore.uuid] == feiqnet.uuid:
            return True
        feiquser.changeName(recvPack[feiqcore.uuid], recvPack[feiqcore.name])

    return True


def sendMsg(ip, msg):
    d = {
        feiqcore.cmd: feiqcore.msg,
        feiqcore.msg: msg,
        feiqcore.uuid: feiqnet.uuid,
        feiqcore.name: feiqnet.name
    }

    feiqnet.sendDict(d, ip)


# 创建主函数
def main():
    print('----3.发送用户上线信息----')
    feiqnet.online()

    print('----4.开启子线程用于获取用户数据----')
    thread = threading.Thread(target=feiqnet.getNetData)
    thread.start()

    # 获取用户输入，然后发送消息
    print('----5.主程序进入循环----')
    while True:
        data = input('fq：')
        data = data.strip()

        if data.startswith('send '):
            datas = data.split(' ', 2)
            if len(datas) < 3:
                print('输入值非法，请重新输入(set [ip] [msg]！')
                continue
            sendMsg(datas[1], datas[2])

        elif data.startswith('setname '):
            datas = data.split(' ', 1)
            datas[1] = datas[1].strip()
            if datas[1].find(' ') != -1:
                print('  名字中不能带空格!')
                continue
            feiqnet.setname(datas[1])

        elif data == 'users':
            feiquser.outputUserList()

        elif data == 'exit':
            break

        elif data == 'clear':
            os.system('clear')

    feiqnet.offline()
    thread.join()


if __name__ == '__main__':
    main()
