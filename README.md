Sorry about my english.

# OVERVIEW
This project is used to authenticate users and manage them.

## This project uses:
- Event driven arquitecture;
- Docker, to run all microservices NB: You can use K8s;
- Rabbitmq (broker), used to manage queues;
- Celery, used to process tasks asyncronously;
- Redis, to make cache;
- Nginx, to make an api gateway;
- Postgres, used to store data;
- FastAPI, to building APIs;
- python, with assyncronous programing.


### Why event driven arquitecture?
This project uses Event driven arquitecture, so that, the project is based on
events, the microservices dont call others directly they use a broker (queue manager)
storing messages in a queues, so that, other microservices called workers will
pull the messages on that queues to process.
Using event driven arquitecture, you can scale all microservices individualy, you can also
scale the Broker using a cluster, for example Rabbitmq can run in a cluster granting more
scalability and avalability to yours project.

# SERVICES
This project have one service called "Auth", this services was divided in
4 microservices: "auth_api", "auth_admin_api", "auth_db_worker", and "email_worker".

### auth_api 
is an Rest API, used to signup and signin users, this  microservice generate 
and manage access and refresh tokens. NB: this microservice must have only read access to database,
and must have read and write access to cache to store access tokens.

### auth_admin_api 
is an Rest API, used to manage all users, only staff users can access
this API. NB: this microservice must have only read access to database, and must have only read
access to cache to validate access tokens.

### auth_db_worker 
is an celery worker, used to run all database transactions (of Auth service) from a queue.
When the microservices "auth_api", "auth_admin_api" want to create, update or delete data from database,
they send the transactions to a queue, and this microservice will pull the transactions from that queue and run.
NB: this microservice must have only write access to database.

### email_worker 
is an celery worker, used to send emails messages from a queue using gmail 
(you can modify the code to use any email server), this microservice can be used by others microservices
to send emails.


## OTHERS SERVICES
This project uses others services, like Broker (Rabbitmq), Cache (Redis), SQL Database (Postgres).
NB: In real production situation this services can be scalable. You can see all arquitecture in the
anexed images.



## HOW TO CONFIGURE AND RUN
To run, open the ".env", and file give values ​​to the environment variables that have "IS NECESSARY" comment.
After that, you can run normaly first time using "docker-compose up --build -d". NB: Same services depends on others, so that
to run same services others must be running.




## OTHERS__INFOS
If you want more info about this project, please read the ReadMe.txt files in others directories, for example: if you want
know more about the microservice "auth_api" you need to read the file AUTH_API/ReadMe.txt . I didnt create users for the cache (redis), and
I used the same database user for all microservices because this is a test project, on a real production sictuation please, create users, groups
and previleges for all microservices. 

### Images
I anexed two (2) images files in this project: 
-"Infra.png", that show the infrastruture of this project and how the containers are connected.
-"Infra_if_we_add_elasticsearch.png", shows other infrastruture, that you can use if you want store data in a elasticsearch
cluster to fast data search, using the database to backup only.

### Others_files
I anexed an postman collection "AUTH.postman_collection.json" to test the API on postman.

## Dev_Infos
- Name: James R. R. Artur;
- Email: ojamesartur@gmail.com ;
- A DevOps and infraestructure enthusiastic.







