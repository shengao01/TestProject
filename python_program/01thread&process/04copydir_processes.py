import os
import sys
from multiprocessing import *

# 通过命令行输入参数
dir1 = sys.argv[1]
dir2 = sys.argv[2]

# 判断文件夹是否存在以及确保目标文件夹存在
if not os.path.isdir(dir1):
    print('dir1 is not a directory')
    exit(1)

if os.path.exists(dir2) and not os.path.isdir(dir2):
    print('dir2 is not a directory')
    exit(1)

if not os.path.isdir(dir2):
    os.mkdir(dir2)


# 拷贝文件
def copyFile(file1,file2):
    rfile = open(file1,'rb')
    wfile = open(file2,'wb')

    while True:
        data = rfile.read(1024)
        if not data:
            break
        wfile.write(data)

    rfile.close()
    wfile.close()

processes = []
# 拷贝目录


def copyDir(dir1,dir2):
    for file in os.listdir(dir1):
        file1 = dir1 + '/' + file
        file2 = dir2 + '/' + file

        if os.path.isfile(file1):
            process = Process(target = copyFile,args=(file1,file2))
            process.start()
            processes.append(process)

        elif os.path.isdir(file1):
            os.mkdir(file2)
            copyDir(file1,file2)

copyDir(dir1,dir2)

for process in processes:
    process.join()
print('copy done')

