# 框架搭建
from socket import *
from threading import *
from multiprocessing import *
import uuid
import os
import getpass

import feiqcore
import feiqnet
import feiquser
import feiqfile
import feiqdir


def handleNetwork(recvPack,ip):

    if recvPack[feiqcore.cmd] == feiqcore.senddirack:
        thread = Thread(target=feiqdir.sendDirThread, args=(recvPack[feiqcore.filename], ip))
        thread.start()
        pass

    elif recvPack[feiqcore.cmd] == feiqcore.senddir:
        if recvPack[feiqcore.uuid] == feiqnet.uuid:
            return True

        d = {
            feiqcore.cmd: feiqcore.senddirack,
            feiqcore.filename: recvPack[feiqcore.filename],
            feiqcore.uuid: feiqnet.uuid,
            feiqcore.name: feiqnet.name
        }

        feiqnet.sendDict(d, ip)
        pass

    elif recvPack[feiqcore.cmd] == feiqcore.sendfileack:
        # 创建线程，发送文件
        thread = Thread(target=feiqfile.sendFileThread, args=(recvPack[feiqcore.filename], ip))
        thread.start()

    elif recvPack[feiqcore.cmd] == feiqcore.sendfile:
        d = {
            feiqcore.cmd: feiqcore.sendfileack,
            feiqcore.filename: recvPack[feiqcore.filename],
            feiqcore.uuid: feiqnet.uuid,
            feiqcore.name: feiqnet.name
        }

        feiqnet.sendDict(d, ip)

    elif recvPack[feiqcore.cmd] == feiqcore.online:
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
        print(('%s (%s) say : %s') % (recvPack[feiqcore.name], ip, msg))

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


def sendFile(ip, filepath):
    d = {
        feiqcore.cmd: feiqcore.sendfile,
        feiqcore.filename: filepath,
        feiqcore.uuid: feiqnet.uuid,
        feiqcore.name: feiqnet.name
    }

    feiqnet.sendDict(d, ip)

def sendDir(ip,dirpath):
    d = {
        feiqcore.cmd: feiqcore.senddir,
        feiqcore.filename: dirpath,
        feiqcore.uuid: feiqnet.uuid,
        feiqcore.name: feiqnet.name
    }

    feiqnet.sendDict(d, ip)


def help():
    print('  help -- 显示帮助')
    print('  exit -- 退出程序')
    print('  send -- 发送消息 send {ip} {msg}')
    print('  sendfile -- 发送文件 sendfile {ip} {filepath}')
    print('  senddir -- 发送目录 senddir {ip} {dirpath}')
    print('  users -- 显示在线用户列表')
    print('  whoami -- 显示我的信息')
    print('  setname -- 修改我的帐号名')
    print('  clear -- 清屏')


# 创建主函数
def main():

    print('----3.发送用户上线信息----')
    feiqnet.online()

    # 启动目录接收线程
    dirrecvprocess = Process(target=feiqdir.recvDirMain)
    dirrecvprocess.start()

    # 启动文件接收线程
    filerecvprocess = Process(target=feiqfile.fileServerThread)
    filerecvprocess.start()

    print('----4.开启子线程用于获取用户数据----')
    thread = Thread(target=feiqnet.getNetData)
    thread.start()





    # 获取用户输入，然后发送消息
    print('----5.主程序进入循环----')
    while True:
        data = input('fq：')
        data = data.strip()

        if len(data) == 0:
            continue

        elif data.startswith('senddir '):
            datas = data.split(' ', 2)
            if len(datas) < 3:
                print('输入错误，请输入要求的格式：send [ip] [filepath]')
                continue

            if not os.path.isdir(datas[2]):
                print('输入错误，请输入要求的格式：send [ip] [filepath]')
                continue

            sendDir(datas[1], datas[2])

        elif data.startswith('sendfile '):
            datas = data.split(' ', 2)
            if len(datas) < 3:
                print('输入错误，请输入要求的格式：send [ip] [filepath]')
                continue
            sendFile(datas[1], datas[2])

        elif data.startswith('send '):
            datas = data.split(' ', 2)
            if len(datas) < 3:
                print('输入值非法，请重新输入(send [ip] [msg]！')
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

        elif data == 'help':
            help()

        elif data == 'whoami':
            print(' ' + feiqnet.name)

        else:
            help()

    dirrecvprocess.terminate()
    filerecvprocess.terminate()


    feiqnet.offline()
    thread.join()

if __name__ == '__main__':
    feiqnet.init_sock()
    main()
