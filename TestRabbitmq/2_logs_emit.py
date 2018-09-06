# coding:utf-8
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 若不指定,则适用于消息群发
# channel.queue_declare(queue='task_queue', durable=True)

# exchange为群发的名称,exchange_type为类型,常用的有fanout/direct/topic等.
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message,
                      )
print(" [x] Sent %r" % message)
connection.close()
