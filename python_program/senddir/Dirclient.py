from socket import *
import os

sock = socket(AF_INET,SOCK_STREAM)
sock.connect(('127.0.0.1',19999))

dirname = ''


def writeByData(sock,data):
    writeLen = 0
    while True:
        ret = sock.send(data[writeLen:])
        writeLen += ret
        if writeLen == len(data):
            break


# 发送文件名长度和内容
def sendFileName(basename):
    data = basename.encode()
    datalen = len(data)
    datalenstr = '%08d'%datalen

    writeByData(sock,datalenstr.encode())
    writeByData(sock, data)


# 发送文件的长度和内容
def sendFileCont(filename):
    filelen = os.path.getsize(filename)
    filelenstr = '%08d'%filelen

    writeByData(sock,  filelenstr.encode())

    rfile = open(filename,'rb')
    while True:
        data = rfile.read(1024)
        if not data:
            break
        writeByData(sock, data)
    rfile.close()


# 发送文件的名字和内容
def sendFile(filename):
    print('filepath:', filename)
    writeByData(sock, 'f'.encode())
    basename = os.path.basename(filename)
    print('sendfile:', basename)
    sendFileName(basename)
    sendFileCont(filename)


# 发送目录的名字
def sendDirName(dirname):
    print('dirpath', dirname)
    basename = os.path.basename(dirname)
    print('send dir', basename)
    writeByData(sock, 'd'.encode())
    sendFileName(basename)


def sendDir(dirname):
    sendDirName(dirname)

    for file in os.listdir(dirname):
        filename = dirname + '/' + file
        print('send filename:', filename)
        if os.path.isdir(filename):
            sendDir(filename)
        elif os.path.isfile(filename):
            sendFile(filename)

    writeByData(sock, 'c'.encode())

sendDir(dirname)
writeByData(sock, 'x'.encode())