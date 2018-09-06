# coding:utf-8
import requests
import nose


def test_jb51():
    url = "http://www.jb51.net/article/66763.htm"
    conn = requests.get(url)
    # conn.request(method="GET", url=url)
    # response = conn.getresponse()
    # res = response.

    print(conn.content)


if __name__ == '__main__':
    nose.runmodule()
