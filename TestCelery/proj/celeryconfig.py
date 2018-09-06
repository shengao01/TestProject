# coding:utf-8


BROKER_URL = 'redis://@127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'

# CELERY_ROUTES = ({
#     'tasks.my_task1': {'queue': 'queue1'},
#     'tasks.my_task2': {'queue': 'queue1'},
#     'tasks.my_task3': {'queue': 'queue2'},
#     },
# )
