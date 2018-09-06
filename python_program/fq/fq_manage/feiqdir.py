from socket import *
import os
from multiprocessing import Process


def writeByData(sock, data):
    writeLen = 0
    while True:
        ret = sock.send(data[writeLen:])
        writeLen += ret
        if writeLen == len(data):
            break


# 发送文件名长度和内容
def sendFileName(basename, sock):
    data = basename.encode()
    datalen = len(data)
    datalenstr = '%08d' % datalen

    writeByData(sock, datalenstr.encode())
    writeByData(sock, data)


# 发送文件的长度和内容
def sendFileCont(filename, sock):
    filelen = os.path.getsize(filename)
    filelenstr = '%08d' % filelen

    writeByData(sock,  filelenstr.encode())

    rfile = open(filename, 'rb')
    while True:
        data = rfile.read(1024)
        if not data:
            break
        writeByData(sock, data)
    rfile.close()


# 发送文件的名字和内容
def sendFile(filename, sock):
    print('filepath:', filename)
    writeByData(sock, 'f'.encode())
    basename = os.path.basename(filename)
    print('sendfile:', basename)
    sendFileName(basename, sock)
    sendFileCont(filename, sock)


# 发送目录的名字
def sendDirName(dirname, sock):
    print('dirpath', dirname)
    basename = os.path.basename(dirname)
    print('send dir', basename)
    writeByData(sock, 'd'.encode())
    sendFileName(basename, sock)


def sendDir(dirname, sock):
    sendDirName(dirname, sock)

    for file in os.listdir(dirname):
        filename = dirname + '/' + file
        print('send filename:', filename)
        if os.path.isdir(filename):
            sendDir(filename, sock)
        elif os.path.isfile(filename):
            sendFile(filename, sock)

    writeByData(sock, 'c'.encode())


def sendDirThread(dirpath, ip):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip, 19999))

    sendDir(dirpath, sock)
    writeByData(sock, 'x'.encode())


# ----------------------------------------------------------


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
    readlen = 0
    wfile = open(filename, 'wb')

    while filelen != readlen:
        rlen = filelen - readlen
        if rlen > 1024:
            rlen = 1024

        data = sock.recv(rlen)
        readlen += len(data)
        wfile.write(data)

    wfile.close()


def recvDir(sock):
    filenamelen = int(readByLen(sock, 8))
    filename = readByLen(sock, filenamelen)
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


def recvDirMain():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('', 19999))
    server.listen(250)

    while True:
        sock, addr = server.accept()
        print('send file from addr', addr)
        process = Process(target=func, args=(sock,))
        process.start()

