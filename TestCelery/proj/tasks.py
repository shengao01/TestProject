# coding:utf-8
import time
from proj import app as celery_app


@celery_app.task
def add(a, b):
    time.sleep(1)
    print("add is running")
    return a+b


@celery_app.task
def mul(a, b):
    time.sleep(1)
    print("mul is running")
    return a*b


@celery_app.task
def my_task1(a, b):
    time.sleep(3)
    print("my_task1 is running")
    return a+b


@celery_app.task
def my_task2(a, b):
    time.sleep(3)
    print("my_task2 is running")
    return a*b


@celery_app.task
def my_task3(a, b):
    time.sleep(3)
    print("my_task3 is running")
    return a-b
