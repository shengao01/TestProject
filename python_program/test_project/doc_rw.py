# coding:utf-8
import chardet

# 基本读写操作
f = open('02_format.py')

# 读取整个文件内容
f_cont = f.read()
print(f_cont)

# 逐行读取,返回值是一个列表
# f_cont1 = f.readlines()
# print(f_cont1)
# fq = open('a.py', 'w')
# fq.writelines(f_cont1)
# fq.close()
char_type = chardet.detect(f_cont)
print(char_type)

# 制作备份文件
# file_name = raw_input('请输入要备份的文件:')
# file = open(file_name, 'r')
#
# file_tail = file_name.rfind('.')
#
# file_type = file_name[file_tail:]
#
# new_file_name = file_name[0:file_tail] + u'[复件]' + file_type
# new_file = open(new_file_name, 'w')
# new_file.write(file.read())
#
# new_file.close()
# file.close()


# weekdays = ['Sunday','Monday','Tuesday','Thursday','Wednesday','Friday','Saturday']
#
# def weekday(year,month,day): #由蔡勒公式计算星期数
#     year = int(year)
#     year = year % 100
#     century = int(year/100)
#     month = int(month)
#     if month == 1 or month == 2: #一二月当成去年的十三月和十四月
#         month = month + 12
#         year = year - 1
#     day = int(day)
#     week = century/4-2*century+year+year/4+26*(month+1)/10+day-1 #蔡勒公式
#     if week < 0:
#         return (week % 7 + 7) % 7
#     else:
#         return week%7

# date = raw_input("Input the date such as 1996.1.1\n")
# year,month,day = date.split('.') #分割日期字符串
# print weekdays[weekday(year,month,day)]
