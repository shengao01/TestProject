# coding:utf-8
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

# 从输入参数指定消息类型, 若符合设定的接收类型,则会被consumer获取到
severtity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='direct_logs',
                      routing_key=severtity,
                      body=message,
                      )
print(" [x] Sent %r" % message)
connection.close()
