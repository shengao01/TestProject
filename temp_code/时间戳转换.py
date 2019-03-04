# coding：utf-8
import time
# 时间戳float型 time_stamp
a = time.time()
print(a)
print(type(a))

# 时间格式化字符串str型
b = time.ctime(a)
print(b)
print(type(b))

# 时间数组 time_array   <class 'time.struct_time'>
c = time.strptime(b, '%a %b %d %H:%M:%S  %Y')
print(c)
print(type(c))

# 时间格式化字符串str型
d = time.strftime('%Y-%m-%d %H:%M:%S', c)
print(d)
print(type(d))

# 时间戳float型 time_stamp
e = time.mktime(c)
print(e)
print(type(e))



