SHELL := /bin/zsh -eu -o pipefail

ARG := $(word 2, $(MAKECMDGOALS))
SERVICE := app

.PHONY: clean up down restart build logs shell manage migrate \
        makemigrations createsuperuser check clean-migrations\
		update_dependencies get_secret_key


get_secret_key:
	docker compose exec app python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"

clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete

up:
	docker compose up --build -d

down:
	docker compose down

restart:
	docker compose restart $(ARG)

logs:
	docker compose logs -f $(ARG)

clean-migrations:
	find . -path '*/migrations/*.py' -not -name '__init__.py' -delete
	find . -path '*/migrations/*.pyc' -delete

shell:
	docker compose exec $(ARG) bash

manage:
	docker compose exec $(SERVICE) python manage.py $(ARG)

migrate:
	docker compose exec $(SERVICE) python manage.py migrate $(ARG)

makemigrations:
	docker compose exec $(SERVICE) python manage.py makemigrations

createsuperuser:
	docker compose exec $(SERVICE) python manage.py createsuperuser

check:
	-uv ruff check .
	-uv ruff format --check .

lint:
	uv ruff check . --fix
	uv ruff format .

update_dependencies:
	docker compose down
	docker compose up -d --build
