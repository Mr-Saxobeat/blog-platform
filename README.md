# Blog Platform

This is a mini blog platform where you can post you ideas.
It's built on Django 4.2.11 and Django Rest Framework 3.15.1, using the django template sytem to the frontend.

# Setup

You can setup the project on docker or manually.

## Docker

Fisrt, make sure you have the 5432 and the 8000 ports free, because its the database and the servers ports used, respectively.

Rename the ``.env-dev`` to ``.env`` and fill up the ``DB_PASSWORD`` and ``SECRET_KEY`` with your values.
You can get a new secret key here: [https://djecrety.ir/](https://djecrety.ir/)

Then, at the root of the repository, you run:

````bash
docker compose up
````

This will compose the docker from the ``docker-compose.yaml`` file.

After the pulling and building you will see something like this:

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
Make sure your browser accepts http connections.