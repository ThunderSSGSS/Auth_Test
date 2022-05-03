from __future__ import absolute_import
from celery import Celery
from .settings import RABBITMQ, BACKEND, DEFAULT_QUEUE


broker=RABBITMQ['USER']+':'+RABBITMQ['PASSWORD']+'@'+RABBITMQ['LOCATION']+'/'+RABBITMQ['VHOST']
backend=BACKEND['LOCATION']+':'+BACKEND['PORT']

app = Celery('email_celery',
             broker='amqp://'+broker,
             backend='redis://'+backend,
             include=['app.tasks'])
app.conf.task_default_queue= DEFAULT_QUEUE