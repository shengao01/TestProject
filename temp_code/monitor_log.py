import os,datetime,json
import traceback
from contextlib import contextmanager
import paramiko
import requests

tencent_dir = "/home/trillion/upload_data/"
cta_dir = "/data/nav"
delta = datetime.timedelta(hours = 4) #设定4小时
HOST = 'http://118.126.100.219'
PORT = 20187
VBO = 'vbo'


def connect_cta():
# 服务器信息，主机名（IP地址）、端口号、用户名及密码
    hostname = "18.205.3.20"
    port = 2015
    username = "cta"
    password = "CTA$2018"
    client = paramiko.SSHClient()
    # 设置策略
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password, compress=True)
    return client.open_sftp()


def sendData(data):
    try:
        requests.post(f"{HOST}:{PORT}/{VBO}", json=json.dumps(data, ensure_ascii=False))
    except:
        traceback.print_exc()


@contextmanager
def scanning():
    now = datetime.datetime.now()
    try:
        yield
        ds = list(os.listdir())
        for d in ds:
            if d[-3:] == "log":
                # print(d)
                # ctime = datetime.datetime.fromtimestamp(os.path.getctime(d))
                ctime = datetime.datetime.fromtimestamp(os.stat(d).st_mtime)
                # print(ctime)
                if ctime >= (now - delta):
                    try:
                        with open(d,mode="r") as fp:
                            content = fp.read()
                            # for line in fp:
                            #     if "ERROR" in line.upper():
                            #         print("haha")
                            #         sendData({'[{}]file'.format(sever_name): d + 'catch an error'})
                            #         break
                    except:
                        with os.open(d, mode="r") as fp:
                            content = fp.read().decode()
                    finally:
                        # print(content)
                        if "ERROR" in content.upper():
                            # print("haha")
                            sendData({'[{}]file'.format(sever_name): d + 'catch an error'})

    finally:
        pass

with scanning():
    sever_name = "tencent"
    os.chdir(tencent_dir)

with scanning():
    sever_name = "cta"
    os = connect_cta()
    os.chdir(cta_dir)












#
#                       .::::.
#                     .::::::::.
#                    :::::::::::
#                 ..:::::::::::'
#              '::::::::::::'
#                .::::::::::
#           '::::::::::::::..
#                ..::::::::::::.
#              ``::::::::::::::::
#               ::::``:::::::::'        .:::.
#              ::::'   ':::::'       .::::::::.
#            .::::'      ::::     .:::::::'::::.
#           .:::'       :::::  .:::::::::' ':::::.
#          .::'        :::::.:::::::::'      ':::::.
#         .::'         ::::::::::::::'         ``::::.
#     ...:::           ::::::::::::'              ``::.
#    ```` ':.          ':::::::::'                  ::::..
#                       '.:::::'
#                    --- 王百亿 ---