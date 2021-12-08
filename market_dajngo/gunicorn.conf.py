import os
### Уточнения
# Слушать указанный ip адрес и порт  '<10.130.0.34:8001>'. Но лучше указать UDS сокет 'unix:/run/gunicorn.sock'
bind = f"0.0.0.0:{os.environ.get('EXTERNAL_WEB_PORT','None')}"
# Путь к `WSGI` приложению  `ИмяГлавногоПриложения.wsgi:application`
wsgi_app = "market_dajngo.wsgi:application"


### Производительность
# Количество рабочих процессов для обработки запросов. Оптимально установить количество процессов по формуле `2-(4xЯдерЦпу)`
workers = 3
# Этот параметр используется для ограничения количества заголовков в запросе до предотвратить DDOS-атаку.
limit_request_fields = 32000
# Ограничьте допустимый размер поля заголовка HTTP-запроса.
limit_request_field_size = 0
# Максимальное количество одновременных клиентов
worker_connections = 1000


### Другие
# Авто перезагрузка сервера при изменении файлов проекта `Django`
reload = True
# Путь для вывода лог данных
# accesslog = "gunicorn_ass.log"
# # Путь для вывода ошибок
# errorlog = "gunicorn_err.log"