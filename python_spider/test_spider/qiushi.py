from urllib import request
import re
import time

req = request.urlopen('')

data = ''



'''
https://image5.pengfu.com/origin/170917/59be453caf1a4.png
https://image5.pengfu.com/thumb/170917/59be452a97a84.png
https://image4.pengfu.com/origin/170917/59be450d4f2f0.gif
//pic.qiushibaike.com/system/pictures/11955/119554979/medium/app119554979.jpg
"//pic.qiushibaike.com/system/pictures/11948/119483689/medium/app119483689.jpg"
"//pic.qiushibaike.com/system/pictures/11955/119553268/medium/app119553268.jpg

http://s9tu.com/images/2017/09/29/IMG_1713f938c.jpg'
http://s9tu.com/images/2017/09/29/IMG_171259382.jpg
http://s9tu.com/images/2017/09/29/IMG_1706ed7d5.jpg

https://up0.xhcdn.com/000/156/320/502_1000.jpg

http://xoimg.co/u/20170913/2319565.gif
'''

ret = re.findall(r'http://xoimg\.co/u/20170913/\d+\.gif', data)
print(ret)
i = 1
for link in ret:
    print(link)
    coment = request.urlopen(link)
    photo = coment.read()
    name = 'photo%d.gif' % i
    file = open('photo/'+name, 'wb')
    file.write(photo)
    file.close()
    i += 1
    time.sleep(2)
