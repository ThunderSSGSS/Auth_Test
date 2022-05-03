___ABOUT_THE_AUTH_DB_WORKER_SERVICE___:
The service "auth_db_worker" is an celery worker used to process database transactions of services: "auth_api" 
and "auth_admin_api". This service pull the transactions from the "broker" service (Rabbitmq) queue. 
You can change the name of the queue in ".env" file on variable "AUTH_DB_TRANSACTIONS_QUEUE".

_______________TASKS___________:
This Worker have 3 tasks:

_____Name: create_object
_______Parameters: tablename, data_dict
_______INFO: this task run create transactions. "data_dict" is a dictionary that
contain the data of the row that will be created.


_____Name: update_object
_______Parameters: tablename, object_id, data_dict
_______INFO: this task run update transactions, "data_dict" is a dictionary that
contain the new datas of the row.


_____Name: delete_object
_______Parameters: tablename, object_id
_______INFO: this task run delete transactions.


____DIRECTORIES___:
The "auth_db_worker/app" dir contain the code of Celery worker.