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


AUTH={
	'SECRET_KEY': os.environ.get('AUTH_SECRET_KEY'),
	'ALGORITHM': os.environ.get('AUTH_ALGORITHM'),
	'COMPLETE_SIGNUP_LINK': os.environ.get('COMPLETE_SIGNUP_LINK')
}

RABBITMQ={
	'USER': os.environ.get('RABBITMQ_USER'),
	'PASSWORD': os.environ.get('RABBITMQ_PASSWORD'),

	'LOCATION': os.environ.get('RABBITMQ_IP'),
	'VHOST': os.environ.get('RABBITMQ_VHOST')
}

RABBITMQ_QUEUES={
	'EMAILS': os.environ.get('EMAILS_QUEUE'),
	'DB_TRANSACTIONS': os.environ.get('DB_TRANSACTIONS_QUEUE')
}