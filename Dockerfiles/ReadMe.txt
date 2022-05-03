___Dockerfiles___:

__Celery/Dockerfile__: creates a image based on python 3.7 alpine, and install the basic celery
libraries.

__Celery_with_sql/Dockerfile: creates a image based on python 3.7 alpine, install the basic celery
libraries and sqlalchemy.

__FastAPI/Dockerfile__: creates a image based on python 3.7 alpine, install the basics FastAPI
libraries and asyncronous sqlalchemy library.

__Filebeat/Dockerfile__: creates a image based on Filebeat official elastic image v8.1.3, and configure it.

__Rabbitmq/Dockerfile__: creates a image based on Rabbitmq official image alpine v3.9.13, and enable the monitoring
plugin.

