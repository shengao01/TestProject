# coding:utf-8
import pika
import time
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


# 声明exchange名称和类型
channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')


result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# severities相当于是秘钥的指定名称, 此例中为通过用户输入指定, 意义为对接收的消息进行筛选
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)


# 从输入参数指定可接收的routing_key,与queue及exchange进行绑定
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)


def callback(ch, method, properties, body):
    print(" [x] Received %r %r" % (method.routing_key, body))

print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
