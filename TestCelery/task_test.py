# coding: utf-8
import time
from celery import Celery

celery_app = Celery("demo", broker="redis://@127.0.0.1:6379/0", backend="redis://@127.0.0.1:6379/1")


@celery_app.task
def my_task1(a, b):
    time.sleep(8)
    print("my_task1 is running...")
    return a+b


@celery_app.task
def my_task2(a, b):
    time.sleep(8)
    print("my_task1 is running...")
    return a*b


@celery_app.task
def my_task3(a, b):
    time.sleep(8)
    print("my_task1 is running...")
    return a-b
