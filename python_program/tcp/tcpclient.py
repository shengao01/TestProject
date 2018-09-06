from socket import *

port = 10010

# 创建
sock = socket(AF_INET,SOCK_STREAM)

# 连接
sock.connect(('127.0.0.1',port))

# 发送
while True:
    msg = input('请输入信息：')
    sock.send(msg.encode())
    data = sock.recv(1024)
    print(data)
# 接收


sock.close()