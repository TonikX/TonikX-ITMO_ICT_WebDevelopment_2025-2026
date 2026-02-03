# Makefile для управления проектом Hotel Management System

.PHONY: help build up down restart logs shell migrate test reset-data backup docs clean

help:  ## Показать это сообщение
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build:  ## Собрать Docker образы
	docker-compose build

up:  ## Запустить контейнеры
	docker-compose up -d

down:  ## Остановить контейнеры
	docker-compose down

restart:  ## Перезапустить контейнеры
	docker-compose restart

logs:  ## Показать логи
	docker-compose logs -f web

shell:  ## Открыть Django shell
	docker-compose exec web python manage.py shell

dbshell:  ## Открыть PostgreSQL shell
	docker-compose exec db psql -U hotel_user hotel_db

migrate:  ## Выполнить миграции
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate

test:  ## Запустить тесты
	docker-compose exec web python manage.py test

test-api:  ## Быстрый тест API endpoints
	bash scripts/test_api.sh

reset-data:  ## Перезагрузить тестовые данные
	bash scripts/reset_data.sh

backup:  ## Создать резервную копию БД
	bash scripts/backup_db.sh

createsuperuser:  ## Создать суперпользователя
	docker-compose exec web python manage.py createsuperuser

collectstatic:  ## Собрать статические файлы
	docker-compose exec web python manage.py collectstatic --noinput

docs:  ## Запустить сервер документации MkDocs
	mkdocs serve

docs-build:  ## Собрать документацию
	mkdocs build

clean:  ## Очистить временные файлы
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf htmlcov/ .coverage site/

clean-all:  ## Полная очистка (включая volumes)
	docker-compose down -v
	rm -rf backups/
	$(MAKE) clean

install:  ## Первоначальная установка
	@echo "Установка проекта..."
	docker-compose up --build -d
	@echo "Ожидание запуска сервисов..."
	sleep 10
	@echo "Проект готов!"
	@echo "Откройте: http://localhost:8000/swagger/"
	@echo "Админка: http://localhost:8000/admin/ (admin / admin123)"

status:  ## Показать статус контейнеров
	docker-compose ps

healthcheck:  ## Проверить здоровье сервисов
	@echo "Проверка API..."
	@curl -s http://localhost:8000/api/ > /dev/null && echo "✓ API работает" || echo "✗ API недоступен"
	@echo "Проверка базы данных..."
	@docker-compose exec db pg_isready -U hotel_user && echo "✓ БД работает" || echo "✗ БД недоступна"

url:  ## Показать полезные URL
	@echo "Полезные ссылки:"
	@echo "  API Root:  http://localhost:8000/api/"
	@echo "  Swagger:   http://localhost:8000/swagger/"
	@echo "  ReDoc:     http://localhost:8000/redoc/"
	@echo "  Admin:     http://localhost:8000/admin/"
	@echo ""
	@echo "Учетные данные:"
	@echo "  Username: admin"
	@echo "  Password: admin123"
