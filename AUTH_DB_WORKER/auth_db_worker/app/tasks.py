from __future__ import absolute_import
from .celery import app
from .database import SessionLocal, User_EDIT
import uuid

def get_db_session():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

def select_crud(tablename):
	#if tablename=="users":
		#return User_EDIT
	return User_EDIT



###############__DATABASE_FUNCTION__###############
@app.task(name='create_object')
def create_object(tablename, data_dict):
	session = next(get_db_session())
	crud_class = select_crud(tablename)
	crud= crud_class(session)
	if crud.validate_create(data_dict):
		crud.create_object(data_dict)

@app.task(name='update_object')
def update_object(tablename, object_id, data_dict):
	session = next(get_db_session())
	crud_class = select_crud(tablename)
	crud= crud_class(session)
	if crud.validate_update(data_dict):
		crud.update_object(object_id,data_dict)

@app.task(name='delete_object')
def delete_object(tablename, object_id):
	session = next(get_db_session())
	crud_class = select_crud(tablename)
	crud= crud_class(session)
	crud.delete_object(object_id)