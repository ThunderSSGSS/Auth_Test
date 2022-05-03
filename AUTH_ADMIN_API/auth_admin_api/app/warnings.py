def not_found_msg(model_name:str):
	return model_name+' not found'

def deleted_msg(model_name:str, id:str):
	return model_name+' '+id+' was deleted'

def altered_msg(model_name:str, id:str):
	return model_name+' '+id+' was altered'

def exist_msg(model_name:str):
	return model_name+' alread exist'

def incorrect_password_msg():
	return 'Incorrect password'

def the_link_key_expired():
	return 'The link expired'

########__VALIDATORS__#########
def invalid_email_msg():
	return 'The email is invalid'

def invalid_password_msg():
	return 'The password is invalid'