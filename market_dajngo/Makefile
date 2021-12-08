# Имя контейнера
host=postgres-db
# Путь к переменным окружения
env_path=__env.env

# Получить ip адрес указанного контейнера
get_ip:
	docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(host)

# Запустить контейнеры а после окночанию отчистить удлаить их
up:
	sudo docker-compose --env-file $(env_path) up && sudo docker-compose rm -fsv;

# Запустить сервер `django`
dj_run:
	python manage.py runserver 0.0.0.0:8080

# Запустить сервер `gunicorn`
dj_gunicorn_run:
	gunicorn  -b 0.0.0.0:8080 --reload market_dajngo.wsgi:application

# Создать миграции в БД
dj_migrate:
	python manage.py migrate && python manage.py flush

# Загрузить данные в БД из дампа
dj_load:
	python manage.py loaddata $(filter-out $@,$(MAKECMDGOALS))

# Создать дамб БД
dj_dump:
	python manage.py dumpdata > dump.json

