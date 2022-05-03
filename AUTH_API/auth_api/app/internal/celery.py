#from celery import shared_task
from app.settings import RABBITMQ, RABBITMQ_QUEUES
from celery import Celery, Task

broker_auth='amqp://'+RABBITMQ['USER']+':'+RABBITMQ['PASSWORD']+'@'+RABBITMQ['LOCATION']+'/'+RABBITMQ['VHOST']

class EmailTask(Task):
	queue=RABBITMQ_QUEUES['EMAILS']

class DatabaseTask(Task):
	queue=RABBITMQ_QUEUES['DB_TRANSACTIONS']

celery_auth = Celery('app_auth', broker=broker_auth)

###############__Email_Tasks__###############
@celery_auth.task(base=EmailTask, name='send_email')
def send_email(to, subject, message):
	return _send_email(to,subject,message)

###############__DATABASE_TASKS__###############
@celery_auth.task(base=DatabaseTask, name='create_object')
def create_object(tablename, data_dict):
	return _create_object(tablename,data_dict)

@celery_auth.task(base=DatabaseTask, name='update_object')
def update_object(tablename, object_id, data_dict):
	return _update_object(tablename,object_id,data_dict)

@celery_auth.task(base=DatabaseTask, name='delete_object')
def delete_object(tablename, object_id):
	return _delete_object(tablename,object_id)