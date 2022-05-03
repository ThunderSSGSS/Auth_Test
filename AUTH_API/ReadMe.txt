___ABOUT_THE_AUTH_API_SERVICE___:
The service "auth_api" is an rest API maked using FastAPI, this service is used to: 
1 - signup and signin the users;
2 - Create access and refresh tokens;
3 - Refresh the tokens.

This service have access to read and write in cache, and access to read only on Database.


____________________ROUTERS_________________:

____ROUTE: /signup/
______ALOWED_METHODS: POST
______SENDED_JSON_OBJECT_FORMAT: {"email" : "string", "password": "string"}
______INFOS: creates a user and send the confirmation link to email.


____ROUTE: /complete_signup/{url_key}
______ALOWED_METHODS: POST
______SENDED_JSON_OBJECT_FORMAT: {"last_password" : "string", "password": "string"}
______INFOS: Activates the user, the "url_key" will be founded in the email. The "last_password" is the password used
to create the user on "/signup/" route. The "password" is the new password for the user. NB: you can repeat the password. 


____ROUTE: /authenticate/
______ALOWED_METHODS: POST
______SENDED_JSON_OBJECT_FORMAT: {"email" : "string", "password": "string"}
______INFOS: Signin the users, return the access and refresh tokens.


____ROUTE: /refresh/
______ALOWED_METHODS: POST
______SENDED_JSON_OBJECT_FORMAT: {"refresh": "string"}
______INFOS: Refresh the access token, return the new access token.


____DIRECTORIES___:
The "auth_api/app" dir contain the code of the api.