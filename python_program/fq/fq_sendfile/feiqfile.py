from socket import *
from threading import *
import os


def writeByData(sock,data):
    writelen = 0

    while True:
        ret = sock.send(data[writelen:])
        writelen += ret
        if writelen == len(data):
            break


def sendFileThread(filepath,ip):
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect((ip,18888))

    filename = os.path.basename(filepath)

    # 1.首先发送文件名长度
    filenameData = filename.encode()
    filenameLen = len(filenameData)
    # 将文件名格式化输出为8个字节的长度
    filenameLenStr = '%08d'%filenameLen
    filenameLenData = filenameLenStr.encode()
    sock.send(filenameLenData)

    # 2.发送文件名
    sock.send(filenameData)

    # 3.发送文件长度
    filename = filepath
    filelen = os.path.getsize(filename)
    filelenStr = '%08d'%filelen
    filelenStrData = filelenStr.encode()
    sock.send(filelenStrData)

    # 4.发送文件内容
    rfile = open(filename,'rb')
    while True:
        data = rfile.read(1024)
        if not data:
            break

        writeByData(sock,data)
    rfile.close()


def readByData(sock,totalLen):
    readLen = 0
    data = b''
    while True:
        readData = sock.recv(totalLen - readLen)
        readLen += len(readData)
        data += readData
        if readLen == totalLen:
            break
    return data.decode()


# 服务客户端的线程
def clientFunc(sock,addr):
    # 1.读文件名的长度
    filenameLen = readByData(sock,8)
    sumLen = int(filenameLen)
    print('文件名长度是:',sumLen)

    # 2.读取文件名
    filename = readByData(sock,sumLen)
    print('文件名是：',filename)
    rfile = open(filename,'wb')

    # 3.读取文件长度
    fileLen = readByData(sock, 8)
    sumLen = int(fileLen)
    print('文件的长度是:', sumLen)

    # 4.读取文件的内容
    readLen = 0
    while True:
        readData = sock.recv(1024)
        rfile.write(readData)
        readLen += len(readData)
        if readLen == sumLen:
            break

    rfile.close()
    sock.close()


def fileServerThread():

    server = socket(AF_INET,SOCK_STREAM)
    server.bind(('',18888))
    server.listen(250)
    print('文件服务器启动')

    while True:
        sock,addr = server.accept()
        print('接收链接')
        thread = Thread(target=clientFunc,args=(sock,addr))
        thread.start()