from os import system, remove, environ
from re import sub


def read_env_file_and_set_from_venv(file_name: str):
	"""Чтение переменных окружения"""
	with open(file_name, 'r', encoding='utf-8') as _file:
		res = {}
		for line in _file:
			tmp = sub(r'^#[\s\w\d\W\t]*|[\t\s]', '', line)
			if tmp:
				k, v = tmp.split('=')
				res[k] = v
	environ.update(res)
	print(res)


def get_ip_container_from_name_container(name_container):
	"""Получить ip адрес контейнера по его имени"""
	system(
			"docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' %s > id.txt" % name_container)
	with open('id.txt', 'r') as _f:
		ip_host = _f.read().replace('\n', '')
	remove('id.txt')
	print(ip_host)
	return ip_host
