#from celery import shared_task
from app.settings import RABBITMQ, RABBITMQ_QUEUES
from celery import Celery, Task

broker_auth='amqp://'+RABBITMQ['USER']+':'+RABBITMQ['PASSWORD']+'@'+RABBITMQ['LOCATION']+'/'+RABBITMQ['VHOST']

class DatabaseTask(Task):
	queue=RABBITMQ_QUEUES['DB_TRANSACTIONS']

celery_auth = Celery('app_auth_admin', broker=broker_auth)

######_________DATABASE_TASKS_________######
#CREATE
@celery_auth.task(base=DatabaseTask, name='create_object')
def create_object(tablename, data_dict):
	return _create_object(tablename,data_dict)

#UPDATE
@celery_auth.task(base=DatabaseTask, name='update_object')
def update_object(tablename, object_id, data_dict):
	return _update_object(tablename,object_id,data_dict)

#DELETE
@celery_auth.task(base=DatabaseTask, name='delete_object')
def delete_object(tablename, object_id):
	return _delete_object(tablename,object_id)