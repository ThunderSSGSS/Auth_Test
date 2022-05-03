___ABOUT_THE_AUTH_ADMIN_API_SERVICE___:
The service "auth_admin_api" is an rest API maked using FastAPI, this service is used to: CRUD
(create, read, update and delete) users. The users created by this API, can signin normaly if 
the attribute or colum called "is_active" is true. Only staff users can access this API.

This service have access to read only on cache, and access to read only on Database.


____________________ROUTERS_________________:
All requests to this api must have the header "Authorization", that contain the access token.

____ROUTE: /admin/users/
______ALOWED_METHODS: POST (creates user), GET (return users)
______PARAMETERS: skip (skip users, default=0), limit (max results numbers, default=100)
______SENDED_JSON_OBJECT_FORMAT: {"email": "string", "password":"string", 
	"is_staff": bool, "is_active": bool}
______INFOS: This route is used to create users and list


____ROUTE: /admin/users/{user_id}
______ALOWED_METHODS: PUT (update the user), GET (return the user), DETELE (delete the user)
______SENDED_JSON_OBJECT_FORMAT: {"email": "string", "is_staff": bool, "is_active": bool, "is_complete": bool}
______INFOS: This route is used to update, get and delete user. The Json format is used in update, 
	all attributes are optional.


____DIRECTORIES___:
The "auth_admin_api/app" dir contain the code of the api.