___ABOUT_THE_EMAIL_WORKER_SERVICE___:
The service "email_worker" is an celery worker used to send emails. This service pull the emails
from the "broker" service (Rabbitmq) queue. You can change the name of the queue in ".env" 
file on variable "EMAILS_QUEUE".


_______________TASKS___________:
This Worker have 1 task:

_____Name: send_email
_______Parameters: to, subject, message
_______INFO: sends email message with the subject, the parameter "to" refer to a destiny
email. Before sends the message, this task print the message on console.



____DIRECTORIES___:
The "email_worker/app" dir contain the python code of the Celery worker.