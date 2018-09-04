from socket import *
from threading import *
import os

server = socket(AF_INET, SOCK_STREAM)
server.bind(('', 18888))
server.listen(250)

# 要求读取多长的数据
def readByLen(sock, totalLen):
    readLen = 0
    data = b''
    while True:
        readdata = sock.recv(totalLen-readLen)
        readLen += len(readdata)
        data += readdata

        if readLen == totalLen:
            break
    return data.decode()


def recvFile(sock):
    filenamelen = int(readByLen(sock, 8))
    filename = readByLen(sock, filenamelen)
    print('recv file:', filename)

    filelen = int(readByLen(sock, 8))
    wfile = open(filename, 'wb')

    readlen = 0
    while filelen != readlen:
        rlen = filelen - readlen
        if rlen > 1024:
            rlen = 1024

        data = sock.recv(rlen)
        readlen += len(data)
        wfile.write(data)

    wfile.close()


def recvDir(sock):
    filenamelen = int(readByLen(sock,8))
    filename = readByLen(sock,filenamelen)
    print('recv dir', filename)
    os.mkdir(filename)
    os.chdir(filename)


def func(sock):
    while True:
        type = sock.recv(1)
        type = type.decode()
        if type == 'd':
            recvDir(sock)

        elif type == 'f':
            recvFile(sock)

        elif type == 'c':
            print('当前文件夹接收完毕')
            os.chdir('..')

        elif type == 'x':
            break

while True:
    sock,addr = server.accept()
    print('send file from addr', addr)
    thread = Thread(target=func, args=(sock,))
    thread.start()



