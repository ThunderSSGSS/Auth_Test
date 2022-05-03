import os


DATABASE={
	'NAME': os.environ.get('DATABASE_NAME'),
	'USER': os.environ.get('DATABASE_USER'),
	'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
	'LOCATION': os.environ.get('DATABASE_SERVER')
}

CACHE={
	'LOCATION': os.environ.get('CACHE_SERVER'),
	'PORT':6379,
	'PREFIX':'auth'
}

RABBITMQ={
	'USER': os.environ.get('RABBITMQ_USER'),
	'PASSWORD': os.environ.get('RABBITMQ_PASSWORD'),

	'LOCATION': os.environ.get('RABBITMQ_IP'),
	'VHOST': os.environ.get('RABBITMQ_VHOST')
}

RABBITMQ_QUEUES={
	'DB_TRANSACTIONS': os.environ.get('DB_TRANSACTIONS_QUEUE')
}