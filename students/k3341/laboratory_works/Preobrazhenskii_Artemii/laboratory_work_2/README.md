# Django template

[![License: MIT](https://img.shields.io/github/license/vintasoftware/django-react-boilerplate.svg)](LICENSE)

## About

A [Django](https://www.djangoproject.com/) project template with a multitude of state-of-the-art libraries and tools:

-   [ruff](https://github.com/astral-sh/ruff) with [pre-commit](https://pre-commit.com/) for automated quality assurance

-   [uv](https://github.com/astral-sh/uv) for fast Python dependency management and environment isolation

-   [Celery](https://docs.celeryq.dev/en/stable/), for background worker tasks

For continuous integration, a [Github Action](https://github.com/features/actions) configuration `.github/workflows/main.yml` is included.

-   PostgreSQL, for DB
-   Redis, for Celery

## Features Catalogue

### Backend

-   `celery` for background worker tasks
-   `django` for building backend logic using Python
-   `djangorestframework` for building a REST API on top of Django
-   `django-upgrade` for automatically upgrading Django code to the target version on pre-commit
-   `django-csp` for setting the draft security HTTP header Content-Security-Policy
-   `django-permissions-policy` for setting the draft security HTTP header Permissions-Policy
-   `django-celery-results` for storing Celery task results in the Django database
-   `django-celery-beat` for managing periodic Celery tasks and schedules in the database
-   `django-defender` for blocking brute force attacks against login
-   `psycopg2-binary` for using PostgreSQL database
-   `redis` for message brokering and caching (used by Celery and Django)
-   `python-dotenv` for loading environment variables from `.env` files
-   `pre-commit` for managing Git hooks for code formatting, linting, and automated checks

## Project bootstrap [![main](https://github.com/preobart/template/actions/workflows/main.yml/badge.svg)](https://github.com/preobart/template/actions/workflows/main.yml) 

-   [ ] Make sure you have Python 3.13 installed
-   [ ] Install Django with `pip install django`, to have the `django-admin` command available
-   [ ] Open the command line and go to the directory you want to start your project in
-   [ ] Start your project using (replace `project_name` with your project name and remove the curly braces):
    ```
    django-admin startproject djangotours . --extension py,json,yaml,toml,lock --name Dockerfile,README.md,.env.example,.gitignore,Makefile,LICENSE,.env,docker-compose.yml,main.yml --template=https://github.com/preobart/template/archive/refs/heads/main.zip
    ```
In the next steps, always remember to replace djangotours with your project's name (in case it isn't yet):
-   [ ] Above: don't forget the `--extension` and `--name` params!
-   [ ] Go into project's root directory: `cd djangotours`
-   [ ] Change the first line of README to the name of the project

After completing ALL of the above, clear the README. Then follow `Running` below.

## Running

### If you are using Docker, you can:

-   Create the migrations for app:
    `make makemigrations`
-   Run the migrations:
    `make migrate`
-   Run the project:
    `make up`
-   To access the logs for each service, run:
    `make logs <service name>` (either `app`, `db`, etc)
-   To stop the project, run:
    `make down`

#### Adding new dependencies

-   Open a new command line window and go to the project's directory
-   Update the dependencies management files by performing any number of the following steps:
-   To add a new dependency, run `docker compose run --rm app bash` to open an interactive shell and then run `uv add {dependency}` to add the dependency. 
-   After updating the desired file(s), run `make update_dependencies` to update the containers with the new dependencies
    > The above command will stop and re-build the containers in order to make the new dependencies effective


### If you are not using Docker:

#### Setup the backend app

-   Open the `.env` file on a text editor and do one of the following:
    -   If you wish to use PostgreSQL locally, fill in the following parameters in the .env file: POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB.
-   Open a new command line window and go to the project's directory
-   Install uv with `pip install uv`, to have the `uv` command available
-   Run `uv venv`, , activate the virtual environment, then run `uv sync`, 

#### Setup Celery

-   `uv run celery --app=djangotours worker --loglevel=info`


#### Setup Redis

-   Ensure that Redis is already installed on your system. Once confirmed, run `redis-server --port 6379` to start the Redis server.
-   If you wish to use Redis for Celery, you need to set the `CELERY_BROKER_URL` environment variable in the `.env` file to `redis://localhost:6379/0`.
    -   The `/0` at the end of the URL specifies the database number on the Redis server. Redis uses a zero-based numbering system for databases, so `0` is the first database. If you don't specify a database number, Redis will use the first database by default.
    -   Note: Prefer RabbitMQ over Redis for Broker, mainly because RabbitMQ doesn't need visibility timeout. See [Recommended Celery Django settings for reliability](https://gist.github.com/fjsj/da41321ac96cf28a96235cb20e7236f6).

#### Run the backend app

-   Go to the project directory
-   Create the migrations for app:
    `python manage.py makemigrations`
-   Run the migrations:
    `python manage.py migrate`
-   Run the project:
    `python manage.py runserver`

### Testing

`make test`

Will run django tests using `--keepdb` and `--parallel`. You may pass a path to the desired test module in the make command. E.g.:

`make test someapp.tests.test_views`

### Adding new pypi libs

To add a new dependency, run `uv add {dependency}`.

## Linting

-   At pre-commit time
-   Manually with `uv run ruff` on project root.

## Pre-commit hooks

-   On project root, run `pre-commit install` to enable the hook into your git repo. The hook will run automatically for each commit.
