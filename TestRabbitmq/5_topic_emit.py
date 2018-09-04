# coding:utf-8
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

severtity = sys.argv[1] if len(sys.argv) > 2 else 'animal.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='topic_logs',
                      routing_key=severtity,
                      body=message,
                      )
print(" [x] Sent %r" % message)
connection.close()
