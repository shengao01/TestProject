# coding:utf-8
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

'''while recv queue_declare set exclusive, no need emit queue_declare'''
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# 适用于指定队列名称
# result = channel.queue_declare(queue='task_queue', durable=True)
# queue_name = result.method.queue
print queue_name

channel.queue_bind(exchange='logs',
                   queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")

print(' [*] Waiting for messages. To exit press CTRL+C')

# channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
