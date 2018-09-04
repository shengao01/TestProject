# coding:utf-8
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)  # durable表示队列持久性
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 是否设置返回标记

channel.basic_qos(prefetch_count=1)  # 公平派遣
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()

# 输出：
# [消费者] waiting for msg .
# [消费者] recv b'hello world'