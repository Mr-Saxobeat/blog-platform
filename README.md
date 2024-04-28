# Blog Platform

This is a mini blog platform where you can post you ideas.

It's built on Django 4.2.11.
For a RESTful API it was used Django Rest Framework 3.15.1.
For a minimal frontend, it was used the django template system, that consume the REST views.
You can check all the api endpoints on the ``/swagger`` endpoint.

## Setup

You can setup the project using docker or manually.

### Docker

Fisrt, make sure you have the 5432 and the 8000 ports free, because its the database and the servers ports used, respectively.
But you change these, see later.

Rename the ``.env-dev`` file to ``.env`` and fill up the ``DB_PASSWORD`` and ``SECRET_KEY`` with your values.
You can get a new secret key here: [https://djecrety.ir/](https://djecrety.ir/)

Then, at the root of the repository, you run:

````bash
docker compose up
````

This will run docker using the ``docker-compose.yaml`` file, that contains a postgres service and the django blog already pointing to the postgres instance.

After the building and the containers running you will see something like this:

```bash
blog-platform-1  |   Applying auth.0002_alter_permission_name_max_length... OK
blog-platform-1  |   Applying auth.0003_alter_user_email_max_length... OK
blog-platform-1  |   Applying auth.0004_alter_user_username_opts... OK
blog-platform-1  |   Applying auth.0005_alter_user_last_login_null... OK
blog-platform-1  |   Applying auth.0006_require_contenttypes_0002... OK
blog-platform-1  |   Applying auth.0007_alter_validators_add_error_messages... OK
blog-platform-1  |   Applying auth.0008_alter_user_username_max_length... OK
blog-platform-1  |   Applying auth.0009_alter_user_last_name_max_length... OK
blog-platform-1  |   Applying auth.0010_alter_group_name_max_length... OK
blog-platform-1  |   Applying auth.0011_update_proxy_permissions... OK
blog-platform-1  |   Applying auth.0012_alter_user_first_name_max_length... OK
blog-platform-1  |   Applying sessions.0001_initial... OK
blog-platform-1  | Watching for file changes with StatReloader

```

Then just go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and you get the blog platform.
**Make sure your browser accepts HTTP connections.**

If you want to run a container only with the django project and setup your own postgres instance, run the compose up command pointing to `docker-compose-without-postgres.yaml` file:

```bash
docker compose -f docker-compose-without-postgres.yaml up
```

--------------------------------------------------------------------------------

### Manually

If you want to run the django server manually, first you need to setup a PostgreSQL database.
Then, rename the `.env-dev` file to `.env` and replace the env vars with your credentials and host:

```txt
# .env file

DB_NAME=# Your database name
DB_USER=# Your username
DB_HOST=# Your database host
DB_PORT=# Your database port
DEBUG=False
SERVER_PORT=8000
DB_PASSWORD=# Your database password
SECRET_KEY=# Your secret key
```

At the root of the repo create a python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual env:

```bash
source .venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Collect the django static files:

```bash
python manage.py collectstatic --no-input
```

Migrate the databse:

```bash
python manage.py migrate
```

And run the server:

```bash
python manage.py runserver
```

You can check the api urls at [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)