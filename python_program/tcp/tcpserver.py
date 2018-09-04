from socket import *
from threading import *

port = 10010
sock = socket(AF_INET,SOCK_STREAM)
sock.bind(('',port))
sock.listen(250)

def clientFunc(sock,addr):
    data = sock.recv(1024)
    sock.send(data)
    sock.close()

while True:
    print('before accept')
    sock,addr = sock.accept()
    thread = Thread(target=clientFunc,args=(sock,addr))
    thread.start()
    print('after accept')

