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

## Redis Setup

- Command to run redis container : docker run --name notes_repo_redis -v redisdata:/data -p 6379:6379 -d 38a44d79682281c78810ce4f57a9a6c65e2307a1c6c4c7719092814b1ab5170f

## Running the project

- Run the project once docker container is started : python manage.py runserver
- Apply all the initial migrations : python manage.py migrate

- Create a superuser : python manage.py createsuperuser

    `Username : notesrepo.notehub@gmail.com`
    `Password : 12345678`
