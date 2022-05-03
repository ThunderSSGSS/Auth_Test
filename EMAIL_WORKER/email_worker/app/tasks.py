from __future__ import absolute_import
from .celery import app
from .settings import EMAIL
import time
import smtplib

@app.task(name='send_email')
def send_email(to, subject, message):
	gmail_user = EMAIL['email']
	gmail_password = EMAIL['password']
	sent_from = gmail_user

	body =message

	email_text = "From: "+sent_from+"\n"
	email_text+="To: "+to+"\n"
	email_text+= "Subject: "+subject+"\n"
	email_text+= "\n"+body
	
	print("THE MESSAGE: ",message)
	server=None
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com',465)
		server.ehlo()
		server.login(gmail_user,gmail_password)
		server.sendmail(sent_from,to,email_text)
		server.close()
		print("____MESSAGE_SENDED")
	except:
		print("____MESSAGE NOT SENDED")
		pass