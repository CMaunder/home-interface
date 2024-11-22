# Home API

Setup

add .env.local:

```
# worker settings

RABBITMQ_USER=charliemaunder
RABBITMQ_PASSWORD=----changeme1-----
RABBITMQ_SERVER=localhost

# rabbitmq settings

RABBITMQ_DEFAULT_USER=charliemaunder
RABBITMQ_DEFAULT_PASS=----changeme1-----

# django settings

DEBUG=1
SECRET_KEY=----changeme2-----
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=----dbnameofchoice----
SQL_USER=charlie
SQL_PASSWORD=----changeme3-----
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
DJANGO_SUPERUSER_PASSWORD=----changeme4-----

# postgres settings

POSTGRES_USER=charlie
POSTGRES_PASSWORD=----changeme3-----
POSTGRES_DB=----dbnameofchoice----
```

## To run locally

migrations are controlled in entrypoint.sh and should be initially uncommented

`docker compose up --build -d`

## Push to dockerhub

Possibly change tag in docker-compose file to version it then:

build the production containers

`docker compose -f docker-compose.prod.yml build && docker compose -f docker-compose.prod.yml push`

## Pull and run on server

If not already there, use sftp, put to move docker-compose.target.yml (rename to docker-compose.yml) and .env.prod onto server then run:

`docker compose down && docker compose pull && docker compose up -d`
