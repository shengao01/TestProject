import time


def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    return str(environ) + '==Hello world from a simple:%s' % time.ctime()