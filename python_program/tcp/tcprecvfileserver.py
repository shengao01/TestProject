from socket import *
from threading import *

port = 10010

server = socket(AF_INET,SOCK_STREAM)
server.bind(('',port))
server.listen(250)


# 服务客户端的线程
def clientFunc(sock,addr):
    # 1.读文件名的长度
    readLen = 0
    data = b''
    while True:
        readData = sock.recv(8-readLen)
        readLen += len(readData)
        data += readData
        if readLen == 8:
            break

    sumLen = int(data.decode())
    print('文件名长度是:',sumLen)

    # 2.读取文件名
    readLen = 0
    data = b''
    while True:
        readData = sock.recv(sumLen - readLen)
        readLen += len(readData)
        data += readData
        if readLen == sumLen:
            break
    filename = data.decode()
    print('文件名是：',filename)

    rfile = open(filename,'wb')

    # 3.读取文件长度
    readLen = 0
    data = b''
    while True:
        readData = sock.recv(8-readLen)
        readLen += len(readData)
        data += readData
        if readLen == 8:
            break

    sumLen = int(data.decode())
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

while True:
    sock,addr = server.accept()
    thread = Thread(target=clientFunc,args=(sock,addr))
    thread.start()