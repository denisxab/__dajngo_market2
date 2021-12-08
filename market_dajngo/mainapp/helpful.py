from typing import Any


class page_obj_cast:
	"""
	Плагиатор страниц
	"""
	
	def __init__(self, paginate_by: int, is_page: int, count: int, max_offer_page: int = 2):
		"""
		:param paginate_by: Колличество элементов на странице
		:param is_page: Текущая страница
		:param count: Всего записей

		| Метод, Атрибут                | Описание                                                                                                  |
		| ----------------------------- | -------------------------------------------------------------- |
		| `page`.number                 | Номер для этой страницы, отсчитываемый от 1.                   |
		| `page`.has_next()             | Возврат `True`если есть следующая страница.                    |
		| `page`.has_previous()         | Возврат `True`если есть предыдущая страница.                   |
		| `page`.has_other_pages()      | Возврат `True`если есть следующая **или** предыдущая страница. |
		| `page`.next_page_number()     | Возвращает номер следующей страницы.                           |
		| `page`.previous_page_number() | Возвращает номер предыдущей страницы.                          |
		| `page`.count                  | Общее количество всех элементов на всех страницах              |
		| `page`.num_pages              | Общее количество страниц.                                      |
		| `page`.page_range             | Итератор для страниц                                           |
		| `page`.max_offer_page         | Сколько страниц предлагать в баре для переключения             |
		| `page`.count                  | Общее количество                                               |
		"""
		self.number = is_page + 1
		self.num_pages = count // paginate_by + (1 if count % paginate_by != 0 else 0)
		self.page_range = range(1, self.num_pages + 1)
		self.has_next = True if self.number * paginate_by < count else False
		self.next_page_number = self.number + 1 if self.number * paginate_by < count else self.number
		self.has_previous = True if self.number > 1 else False
		self.previous_page_number = self.number - 1 if self.number > 1 else self.number
		self.has_other_pages = True if self.has_next or self.has_previous else False
		self.max_offer_page = (max_offer_page * -1, max_offer_page)
		self.count = count
	
	@staticmethod
	def valid_page(page) -> int:
		"""
		Отсчет начинается с 0
		:param page: page_obj_cast.valid_page(request.GET.get("page"))
		"""
		if page is not None and page.isdigit() and int(page) > 0:
			page = int(page) - 1
			return page
		else:
			return 0
	
	def __str__(self):
		return str(self.__dict__)


def dictfetchall(cursor) -> list[dict[str, Any]]:
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
	]
