#! /bin/bash

# Создать миграции
python manage.py makemigrations --no-input
# Применить миграции
python manage.py migrate --no-input

# Запустить сервер djnago
# python manage.py runserver 0.0.0.0:8000

# Запустить сервер gunicorn
gunicorn -c gunicorn.conf.py
