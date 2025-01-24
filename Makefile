.PHONY: migrate
migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

run-server:
	python manage.py runserver 0.0.0.0:8000
