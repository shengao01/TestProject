import time


def app(envrion, start_response):
    status = '200 OK'
    response_header = [('Content-Type', 'text/html')]
    start_response(status, response_header)
    return str(envrion) + 'a message from frame:%s' % time.ctime()

# 模块调用
module_name = 'my_web'
func_name = 'app'
my_web_module = __import__(module_name)
app = getattr(my_web_module, func_name)

# 模块相互调用
def start_response(status,response_header):

    headers = [status, response_header]
