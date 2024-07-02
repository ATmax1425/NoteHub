# NoteHub

The complete SRS of the application is attached in the repository.

# Setting up the project

This project uses a potgres database running in a docker container.

Version : 16

Database : notehub

Username : postgres

Password : 12345678

HOST : localhost

PORT : 5432

Command to run postgres container : docker run --name notes_repo_postgres -e POSTGRES_PASSWORD=12345678 -p 5432:5432 -v pgdata:/var/lib/postgresql/data -d f23dc7cd74bd7693fc164fd829b9a7fa1edf8eaaed488c117312aef2a48cafaa