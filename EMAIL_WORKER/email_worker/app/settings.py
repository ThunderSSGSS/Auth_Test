import os

RABBITMQ={
	'USER': os.environ.get('RABBITMQ_USER'),
	'PASSWORD': os.environ.get('RABBITMQ_PASSWORD'),

	'LOCATION': os.environ.get('RABBITMQ_IP'),
	'VHOST': os.environ.get('RABBITMQ_VHOST')
}

DEFAULT_QUEUE = os.environ.get('WORKER_DEFAULT_QUEUE')

BACKEND={
	'LOCATION': os.environ.get('CACHE_SERVER'),
	'PORT': os.environ.get('CACHE_PORT')
}

EMAIL={
	'email':os.environ.get('SENDER_GMAIL'),
	'password':os.environ.get('SENDER_GMAIL_PASSWORD')
}

