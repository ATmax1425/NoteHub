# NoteHub

The complete SRS of the application is attached in the repository.

# Setting up the project

## Database Setup

This project uses a potgres database running in a docker container.

- Version : 16
- Database : notehub
- Username : postgres
- Password : 12345678
- HOST : localhost
- PORT : 5432
- Command to run postgres container : docker run --name notes_repo_postgres -e POSTGRES_PASSWORD=12345678 -p 5432:5432 -v pgdata:/var/lib/postgresql/data -d f23dc7cd74bd7693fc164fd829b9a7fa1edf8eaaed488c117312aef2a48cafaa
sudo docker run --name notes_repo_postgres -e POSTGRES_PASSWORD=12345678 -p 5432:5432 -v pgdata:/var/lib/postgresql/data -d postgres:latest

## Redis Setup

- Command to run redis container : docker run --name notes_repo_redis -v redisdata:/data -p 6379:6379 -d 38a44d79682281c78810ce4f57a9a6c65e2307a1c6c4c7719092814b1ab5170f
sudo docker run --name notes_repo_redis -v redisdata:/data -p 6380:6379 -d redis:latest

-p 6380:6379, this is what happens:
6380: This is the port on the host machine (your local machine or server).
6379: This is the port inside the Docker container.

## Elastic Search Setup

- Command to create network for elastic : docker run network create
- Command to run docker container : docker run --name notes_repo_elastic --net elastic -p 9200:9200 -d -m 1GB -v es_data:/usr/share/elasticsearch/data 482b5962b08aec7c83a8af3c8aa2213d9a55ff6d6fea7ae2c2fcd9721dbf7299
sudo docker network create elastic
sudo docker run --name notes_repo_elastic --net elastic -p 9200:9200 -d -m 1GB -v es_data:/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:8.4.1

## Running the project

add python requirements.txt 
Django
pip install elasticsearch-dsl
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


- Run the project once docker container is started : python manage.py runserver
- Apply all the initial migrations : python manage.py migrate

- Create a superuser : python manage.py createsuperuser

    `Username : notesrepo.notehub@gmail.com`
    `Password : 12345678`
