# Blog Platform

This is a mini blog platform where you can post you ideas.
It's built on Django 4.2.11 and Django Rest Framework 3.15.1, using the django template sytem to the frontend.

# Setup

You can setup the project on docker or manually.

## Docker

You can run docker compose at the root of the repository. 

Fisrt, make sure you have the 5432 and the 8000 ports free, because its the database and the servers ports used, respectively.

````bash
docker compose up
````

After the pulling and building you will see something like this:

```bash
Attaching to blog-db-1, blog-platform-1
blog-db-1        | 
blog-db-1        | PostgreSQL Database directory appears to contain a database; Skipping initialization
blog-db-1        | 
blog-db-1        | 2024-04-27 14:01:42.741 UTC [1] LOG:  starting PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
blog-db-1        | 2024-04-27 14:01:42.742 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
blog-db-1        | 2024-04-27 14:01:42.742 UTC [1] LOG:  listening on IPv6 address "::", port 5432
blog-db-1        | 2024-04-27 14:01:42.743 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
blog-db-1        | 2024-04-27 14:01:42.748 UTC [29] LOG:  database system was shut down at 2024-04-27 13:57:07 UTC
blog-db-1        | 2024-04-27 14:01:42.754 UTC [1] LOG:  database system is ready to accept connections
blog-platform-1  | 
blog-platform-1  | 161 static files copied to '/blog-platform/static'.
blog-platform-1  | Operations to perform:
blog-platform-1  |   Apply all migrations: admin, api, auth, contenttypes, sessions
blog-platform-1  | Running migrations:
blog-platform-1  |   No migrations to apply.
blog-platform-1  | Watching for file changes with StatReloader
```

Then just go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)