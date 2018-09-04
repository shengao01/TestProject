import socket
import re
import sys
import gevent
from gevent import monkey

# 打补丁
monkey.patch_all()


class WSGIServer(object):
    def __init__(self, port, root_path, app):
        # 创建tcp的套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定信息
        self.server_socket.bind(("", port))
        # 监听变为被动的套接字
        self.server_socket.listen(250)
        self.documents_root = root_path

        self.app = app

    def run_forever(self):
        while True:
            # accpet
            new_socket, new_add = self.server_socket.accept()
            gevent.spawn(self.handle_with_request, new_socket)

    def handle_with_request(self, new_socket):
        # 长连接 有多次的数据需要处理
        while True:
            # 接受数据
            recv_data = new_socket.recv(2048)
            # 判断是否有数据 然后进行解码
            if not recv_data:
                new_socket.close()
                return

            request = recv_data.decode()
            # print(request)
            request_lines = request.splitlines()
            for i, line in enumerate(request_lines):
                print(i, line)
            # 正则表达式 解析发送过来的请求
            #  GET / HTTP/1.1
            # GET /index.html HTTP/1.1
            # POST /xxx.html
            # GET /home/show_goods.html
            # GET /home/logo.png
            # [^ ]
            ret = re.match(r"([^/]*)([^ ]*)", request_lines[0])
            file_path = ret.group(2)
            if file_path == "/":
                file_path = "/index.html"
            print("++++++++++++++++文件的路径:", file_path)
            # 找到对应的文件 打开文件读取数据 返回给客户端
            if not file_path.endswith(".py"):
                try:
                    f = open(self.documents_root + file_path, "rb")
                except Exception as ret:
                    print("打开文件失败:", ret)
                    # 404
                    response_body = "sorry,没有你要的文件"

                    response_header = "HTTP/1.1 404 Not Found\r\n"
                    response_header += "Content-Type: text/html; charset=utf-8\r\n"
                    response_header += "Content-Length: %d\r\n" % len(response_body.encode())
                    response_header += "\r\n"

                    response = response_header + response_body
                    new_socket.send(response.encode())
                    # close
                    # new_socket.close()

                else:
                    content = f.read()
                    response_body = content

                    response_header = "HTTP/1.1 200 OK\r\n"
                    response_header += "Content-Type: text/html; charset=utf-8\r\n"
                    response_header += "Content-Length: %d\r\n" % len(response_body)
                    response_header += "\r\n"

                    new_socket.send(response_header.encode())
                    new_socket.send(response_body)
                    # new_socket.close()
                    # finally:
                    #     new_socket.close()

            else:
                envi = {'when i see'}
                response_body = self.app(envi, self.start_response)
                response_header = 'HTTP/1.1 %s\r\n' % self.headers[0]

                for item in self.headers[1]:
                    response_header += '%s:%s\r\n' % (item[0], item[1])
                response_header += 'Content-Length:%d\r\n' % len(response_body)
                response_header += '\r\n'
                response = response_header + response_body
                new_socket.send(response.encode())

    def start_response(self, status, response_headers):
        self.headers = [status, response_headers]


def main():
    """整体的流程控制"""
    if len(sys.argv) == 3:
        port_str = sys.argv[1]
        if port_str.isdigit():
            port = int(port_str)
        else:
            print("请输入正确的端口号")
            return

        params = sys.argv[2]
        ret = re.match(r'(.*):(.*)', params)
        module_name = ret.group(1)
        func_name = ret.group(2)
        my_web_module = __import__(module_name)
        app = getattr(my_web_module, func_name)

    else:
        print("请以 python3 xxx.py **** 方式运行服务器")
        return

    # 实例化服务对象
    wsgi_server = WSGIServer(port, "./html", app)
    wsgi_server.run_forever()


if __name__ == '__main__':
    main()