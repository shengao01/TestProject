# coding=utf-8

from socket import *
import uuid
import getpass
import feiqcore
import feiquser
import my_fq

print('----2.网络及用户信息初始化----')
# 初始化相关属性
uuid = str(uuid.uuid1())
name = getpass.getuser()
port = 18888
bIP = '192.168.17.255'


# 发送与绑定端口及广播
sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('',port))
sock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)


# 负责接收和发送文件
# 发送上线信息
def sendDict(d,ip = bIP):
    data = str(d).encode()
    sock.sendto(data, (ip, port))


def online():
    onlineMsg = {
        feiqcore.cmd:feiqcore.online,
        feiqcore.name:name,
        feiqcore.uuid:uuid
    }
    sendDict(onlineMsg)


# 发送下线信息
def offline():
    offlineMsg = {
        feiqcore.cmd:feiqcore.offline,
        feiqcore.name:name,
        feiqcore.uuid:uuid
    }
    sendDict(offlineMsg)


# 发送接收上线后反馈信息
def onlineack(ip):
    onlineackMsg = {
        feiqcore.cmd: feiqcore.onlineack,
        feiqcore.name: name,
        feiqcore.uuid: uuid
    }
    sendDict(onlineackMsg,ip)


# 获取网络输入
def getNetData():
    while True:
        data,addr = sock.recvfrom(8192)
        recvPack = eval(data.decode())

        ret = my_fq.handleNetwork(recvPack,addr[0])
        if ret == False:
            break


def setname(n):
    global name
    name = n

    setnameMsg = {
        feiqcore.cmd : feiqcore.setname,
        feiqcore.name : name,
        feiqcore.uuid : uuid
    }
    sendDict(setnameMsg)
