# coding:utf-8
import pika
import time
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='topic_logs',
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
