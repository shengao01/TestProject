from socket import *

soc = socket(AF_INET, SOCK_DGRAM)

dest_addr = ('192.168.220.129', 8080)

send_data = 'hello from client'

soc.sendto(send_data.encode('utf-8'), dest_addr)

soc.close()
