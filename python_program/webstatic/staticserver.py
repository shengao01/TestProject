from socket import *
import re
import sys

class WSGIserver(object):
    def __init__(self, port, root_path):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(('', port))
        self.server_socket.listen(250)
        self.root = root_path

    def run_forever(self):
        while True:
            new_socket, new_add = self.server_socket.accept()
            recv_data = new_socket.recv(2048)
            if not recv_data:
                new_socket.close()
                continue
            request = recv_data.decode()
            # 将代码按行分割
            request_lines = request.splitlines()
            for i, line in enumerate(request_lines):
                print(i, line)

            # 读取第一行代码，并提取出请求的文件
            ret = re.match(r'([^/]*)([^ ]*)', request_lines[0])
            file_path = ret.group(2)
            if file_path == '/':
                file_path = '/index.html'
            print('----文件路径为：', file_path)

            try:
                f = open(self.root + file_path, 'rb')
            except Exception as ret:
                print('打开文件失败：', ret)

                response_header = 'HTTP/1.1 200 OK\r\n'
                response_header += 'Content_Type:text/html; charset=utf-8\r\n'
                response_header += '\r\n'
                response_body = 'sorry,no such file found'
                response_data = response_header + response_body
                new_socket.send(response_data.encode())

            else:
                content = f.read()
                # 如果请求的是文件，则读取文件内容并发送
                response_header = 'HTTP/1.1 200 OK\r\n'
                response_header += 'Content_Type:text/html; charset=utf-8\r\n'
                response_header += '\r\n'
                new_socket.send(response_header.encode())
                new_socket.send(content)

            finally:
                new_socket.close()

def main():
    if len(sys.argv) == 2:
        port_str = sys.argv[1]
        if port_str.isdigit():
            port = int(port_str)
        else:
            print('请输入正确的端口号')
            return
    else:
        print("请以 python3 xxx.py 8888 方式运行服务器")

    wsgi_server = WSGIserver(port,'./html')
    wsgi_server.run_forever()

if __name__ == '__main__':
    main()
