from socket import *
import os

port = 10010
sock = socket(AF_INET,SOCK_STREAM)
sock.connect(('127.0.0.1',port))

filename = input('请输入要发送到服务器的文件路径：')

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
filelen = os.path.getsize(filename)
filelenStr = '%08d'%filelen
filelenStrData = filelenStr.encode()
sock.send(filelenStrData)

def writeByData(sock,data):
    writelen = 0

    while True:
        ret = sock.send(data[writelen:])
        writelen += ret
        if writelen == len(data):
            break

# 4.发送文件内容

rfile = open(filename,'rb')
while True:
    data = rfile.read(1024)
    if not data:
        break

    writeByData(sock,data)
rfile.close()