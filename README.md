# Blog Platform

This is a mini blog platform where you can post you ideas.

It's built on Django 4.2.11.
For a RESTful API it was used Django Rest Framework 3.15.1.
For a minimal frontend, it was used the django template system, that consume the REST views.
You can check all the api endpoints at the ``/swagger`` endpoint.

After your setup, you can create an account, create your posts and comment on others posts.

## Setup

You can setup the project using docker or manually.

### Docker

1. First, make sure you have the **5432** and the **8000** ports free, because its the database and the servers ports used, respectively.
2. Rename the root file ``.env-dev`` to ``.env``.
3. In the ``.env`` file fill up the ``DB_PASSWORD`` with any password, that will be used as the database password.
4. In the ``.env`` file fill up the ``SECRET_KEY`` with a django secret key. You can get a new django secret key here: [https://djecrety.ir/](https://djecrety.ir/)
5. Then, at the root of the repository, you run the following command. This will run docker using the ``docker-compose.yaml`` file, that contains a postgres service and the django blog already pointing to its postgres instance.
````bash
docker compose up
````
6. After the building and the containers running you will see something like this:
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

**Make sure your browser accepts HTTP connections.**

Then just go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and you get the blog platform.

You can check the api urls at [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/).

--------------------------------------------------------------------------------

### Manually

1. First you need to setup a PostgreSQL database.
2. Then, rename the root file `.env-dev` to `.env`
3. Replace the env vars on the `.env` file with your database infos:
```txt
# /.env file
DB_NAME=# Your database name
DB_USER=# Your username
DB_HOST=# Your database host
DB_PORT=# Your database port
DEBUG=False
SERVER_PORT=8000
DB_PASSWORD=# Your database password
SECRET_KEY=# Your secret key
```
4. At the root of the repo create a python virtual environment:
```bash
python -m venv .venv
```
5. Activate the virtual env:
```bash
source .venv/bin/activate
```
6. Install the requirements:
```bash
pip install -r requirements.txt
```
7. Collect the django static files. If here you get the `PermissionError`, don't bother and move on.
```bash
python manage.py collectstatic --no-input
```
8. Migrate the databse:
```bash
python manage.py migrate
```
9. And run the server:
```bash
python manage.py runserver
```

**Make sure your browser accepts HTTP connections.**

Then just go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and you get the blog platform.

You can check the api urls at [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/).

### Using a outside client to the backend api:

As a non authenticated user you can make requests to the `/posts/`endpoint.

But, to make authenticated requests to the api first you need to authenticate:
1. Make a POST request to `/api-token-auth/` with a body like the following:
```json
{
    "username": "your-username",
    "password": "your-password"
}
```
2. Store the returned token
3. To make any other authenticated request, set the token in header with the key `Authorization` and the value with `Token <your-token>`
4. Note the value has a white space between `Token` and the token itself.
5. You're ready to use the core backend with your client!

### Test coverage

The tests were created only for the `api/views.py` and `api/permissions.py` files because the main purpose was to test only
the api side of the project.

You can run the tests with the command:
```bash
python manage.py test
```

You can check the test coverage of the said files by running:
```
coverage run --source='api' manage.py test api
```

And check the report:
```
coverage report
```