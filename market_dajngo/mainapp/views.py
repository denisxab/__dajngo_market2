from typing import Any, Optional

from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
# Create your views here.
from django.db.models.query import RawQuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from mainapp.helpful import page_obj_cast
from mainapp.models import Product, CategoryProduct


class DetailProduct(View):
	template_name = "mainapp/detail_prodcut.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	model = Product  # Какую модель используем
	context_object_name = "products"
	
	def get(self, request: WSGIRequest, pk: int):
		"""
		В методе обрабатывается GET запрос
		request.method == "GET"
		"""
		return render(request,
		              template_name=self.template_name,
		              context=self.get_context_data(pk), )
	
	def get_raw_queryset(self, pk: int):
		queryset: RawQuerySet = self.model.objects.raw("""
		SELECT  prod.id_prod AS id, name, price, is_publish, array_agg(path_photo) AS array_path_photo
		FROM (SELECT id AS id_prod, name, price, is_publish
		      FROM mainapp_product
		      WHERE id = %s) AS prod
		         JOIN mainapp_photoproduct ON prod.id_prod = mainapp_photoproduct.id_product_id
		GROUP BY prod.id_prod, name, price, is_publish ;
		""", (pk,))
		
		# Обьеденить товар с фотографиями
		# dict_obj = self.model.unit_produce_with_photo(self.queryset)
		return queryset
	
	def get_context_data(self, pk, **kwargs) -> dict[str, Any]:
		"""
		Сформировать контекст для шаблона `html`
		"""
		context = {
				self.context_object_name: self.get_raw_queryset(pk),
		}
		return context


class ListProduct(View):
	template_name = "mainapp/lenta.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	
	model = Product  # Какую модель используем
	context_object_name = "products"  # Имя для шаблона, в котором храниться запрос из БД
	
	paginate_by = 2  # Сколько объектов на одной странице
	paginator = page_obj_cast  # Какой плагиатор использовать (Кастомный)
	max_offer_page = 2  # Сколько цифр страниц предлагать для переключения
	
	def get(self, request: WSGIRequest, **kwargs):
		"""
		В методе обрабатывается GET запрос
		request.method == "GET"
		
		- http://<>/?page=1
		"""
		# Проверить корректность запроса `GET` запроса, и получить из него номер страницы.
		# Если некорректный запрос, то вернут page=0
		page: int = self.paginator.valid_page(request.GET.get("page"))
		# Получить строку для поиска
		query_search: str = request.GET.get('RequestSearchText', '')
		# Получить категорию
		query_category_id: int = int(request.GET.get('RequestCategory', 0))
		
		return render(request,
		              template_name=self.template_name,
		              context=self.get_context_data(page, query_search, query_category_id))
	
	def get_raw_queryset(self, page: int, query_search: str, query_category: int) -> Optional[RawQuerySet]:
		"""
		Запросы в БД
		:param query_category:
		:param query_search:
		:param page: Текущая страница
		
		"""
		queryset: Optional[RawQuerySet] = None
		# Проверяем есть ли поисковой запрос
		if not query_search:
			# Проверяем нужен ли поиск по категория
			if not query_category:
				# Получаем объекты. С учетом страницы.
				queryset: RawQuerySet = self.model.objects.raw("""
					SELECT prod.id_prod AS id, name, price, is_publish, array_agg(path_photo) AS array_path_photo
					FROM (SELECT id AS id_prod, name, price, is_publish
					      FROM mainapp_product
					      LIMIT %s  OFFSET %s) AS prod
					         JOIN mainapp_photoproduct ON
					    prod.id_prod = mainapp_photoproduct.id_product_id
					
					GROUP BY prod.id_prod, name, price, is_publish
					ORDER BY prod.name;
					""", [self.paginate_by, self.paginate_by * page])  # PostgreSQL
			else:
				# Если Нужно вернуть товары из одной категории
				queryset: RawQuerySet = self.model.objects.raw("""
					SELECT prod.id_prod AS id, name, price, is_publish, array_agg(path_photo) AS array_path_photo
					FROM (SELECT id AS id_prod, name, price, is_publish, id_category_product_id
					      FROM mainapp_product WHERE id_category_product_id=%s
					      LIMIT %s  OFFSET %s ) AS prod
					         JOIN mainapp_photoproduct ON
					    prod.id_prod = mainapp_photoproduct.id_product_id

					GROUP BY prod.id_prod, name, price, is_publish
					ORDER BY prod.name;
					""", [query_category, self.paginate_by, self.paginate_by * page])
		
		else:
			# Возвращаем только искомые товары
			queryset: RawQuerySet = self.model.objects.raw("""
				SELECT prod.id_prod          AS id,
				       name,
				       price,
				       is_publish,
				       array_agg(path_photo) AS array_path_photo
				
				FROM (
				         SELECT id AS id_prod, name, price, is_publish
				         FROM mainapp_product
				         WHERE name ILIKE  concat('%%',%s,'%%')
				         LIMIT %s OFFSET %s
				     ) AS prod
				         JOIN mainapp_photoproduct ON
				    prod.id_prod = mainapp_photoproduct.id_product_id
				
				GROUP BY prod.id_prod, name, price, is_publish
				ORDER BY prod.name;
				""", [query_search, self.paginate_by, self.paginate_by * page])  # PostgreSQL
		
		return queryset
	
	def get_context_data(self, page: int, query_search: str, query_category_id: int, **kwargs) -> dict[str, Any]:
		"""
		Сформировать контекст для шаблона `html`
		"""
		
		# Получить необходимое колличество товаров
		count_all: int = self.get_count_base(query_search, query_category_id)
		
		context = {
				# Запрос из БД
				self.context_object_name: self.get_raw_queryset(page, query_search, query_category_id),
				# Эхо ответ в форму поисковой строки
				"query_search"          : f"{query_search}" if query_search else '',
				#  Список категорий
				"list_category"         : self.get_category_from_data_base(),
				# Данные для пагинации
				"page_obj"              : self.paginator(self.paginate_by, page, count_all, self.max_offer_page),
				# Дополнительный GET путь для страницы
				'href_page'             :
					f"&RequestSearchText={query_search}" if query_search else '' +
					                                                          f"&RequestCategory={query_category_id}" if query_category_id else '',
				# Id выбранной категории
				'select_id_category'    : query_category_id,
		}
		return context
	
	###
	
	def get_count_base(self, query_search: str, query_category: int, ) -> int:
		"""
		Отвечает за логику получения нужного количества товаров.
		"""
		count_all: int = 0
		
		if not query_search:
			if not query_category:
				# Кешируем общее количество записей
				count_all = self._get_count_all()
			else:
				count_all = self._get_count_category(query_category)
		else:
			# Получаем колличество только для искомых товаров
			count_all = self._get_count_search(query_search)
		return count_all
	
	def _get_count_all(self) -> int:
		"""
		Получить колличество всех записей в таблице
		"""
		_name_ch = "count_all_ch"
		
		count_all = cache.get(_name_ch)
		if not cache.get(_name_ch):
			count_all = cache.get_or_set(
					_name_ch,
					self.model.objects.raw("""
							SELECT 1 AS id, count(id) AS cont
								FROM mainapp_product;
					""")[0].cont
					, timeout=60)
		
		return count_all
	
	def _get_count_category(self, query_category: int) -> int:
		"""
		Получить колличество записей по указанной категории
		"""
		return self.model.objects.raw("""
							SELECT 1 AS id, count(id) AS cont
								FROM mainapp_product WHERE id_category_product_id=%s ;
					""", [query_category])[0].cont
	
	def _get_count_search(self, query_search: str) -> int:
		"""
		Получить колличество записей по искомому слову
		"""
		return self.model.objects.raw("""
			SELECT 1 AS id, count(id)  AS cont
				FROM mainapp_product
				    WHERE name ILIKE concat('%%',%s,'%%')
		""", [query_search])[0].cont
	
	###
	@staticmethod
	def get_category_from_data_base() -> list[CategoryProduct]:
		"""
		Получить список категорий
		"""
		_name_ch = "list_category_ch"
		
		list_category = cache.get(_name_ch)
		if not cache.get(_name_ch):
			sql_req = CategoryProduct.objects.raw("""
					SELECT cet.id AS id ,cet.name AS name_cate, count(id_category_product_id) AS cout_cate
					FROM mainapp_categoryproduct cet
					         JOIN mainapp_product prod
					             ON prod.id_category_product_id = cet.id
					GROUP BY cet.id , cet.name;
							""")
			list_category = cache.get_or_set(
					_name_ch,
					[dict(cow.__dict__) for cow in sql_req]
					, timeout=60)
		return list_category


class BasketServer(View):
	# template_name = "mainapp/.html" # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	
	# model =  # Какую модель используем
	# queryset = .objects. # Получаем данные из БД
	
	def post(self, request: WSGIRequest, ):
		"""
		В методе обрабатывается POST запрос
		request.method == "POST"
		"""
		
		# Получаем корзину пользователя
		UserBasket = request.session.get("UserBasket", '')
		# Получаем  id товара
		id_product = int(request.POST.get('id_product', 0))
		# Получаем флаг который указывает что делать с запросом
		response_flag = request.POST.get('flag')
		
		if response_flag == "AddProductInBasket":
			# Если есть корзина, то добавляем элемент в массив
			if UserBasket:
				request.session["UserBasket"]['list_select_product'].append(id_product)
			# Если нет корзины, то создаем массив с товаром
			else:
				request.session["UserBasket"] = {'list_select_product': [id_product]}
		
		elif response_flag == "DeleteProductInBasket":
			# Если есть корзина, то удаляем элемент в массив
			if UserBasket:
				request.session["UserBasket"]['list_select_product'].remove(id_product)
			# Если нет корзины, то создаем пустой массив с товароми
			else:
				request.session["UserBasket"] = {'list_select_product': []}
		
		# Помечаем, что данные в сессии изменились
		request.session.modified = True
		# Возвращаем `Json` объект
		return JsonResponse({"basket": request.session.get("UserBasket", '')}, status=200)
	
	def get(self, request: WSGIRequest):
		res = request.session.get("UserBasket", None)
		return JsonResponse({"basket": res}, status=200)


class Basket(View):
	template_name = "mainapp/basket.html"  # Путь к шаблону `html`
	http_method_names = ["get"]  # Список методов HTTP, которые обрабатывает класс.
	
	model = Product  # Какую модель используем
	context_object_name = "basket"  # Имя для шаблона, в котором храниться запрос из БД
	
	def get(self, request: WSGIRequest):
		basket: Optional[dict] = request.session.get("UserBasket", None)
		
		return render(request, self.template_name, self.get_context_data(basket))
	
	def get_context_data(self, basket: Optional[dict]):
		context = {
				self.context_object_name: self.get_raw_queryset(basket['list_select_product']) if basket.get(
					'list_select_product') else '',
		}
		return context
	
	def get_raw_queryset(self, basket_list_id: list) -> list:
		#  Создаем `%s` для вставки `id` товаров.
		templates_sql = ",".join(["%s" for _x in range(len(basket_list_id))])
		#  Запрос в БД.
		res_db = self.model.objects.raw(
				f"""
		SELECT prod.id AS id, name, price,  array_agg(path_photo) AS array_path_photo
		FROM (

		         SELECT name,
		                id,
		                price
		         FROM market.public.mainapp_product
		         WHERE id IN  ({templates_sql})

		     ) AS prod
		         JOIN mainapp_photoproduct ON
		    prod.id= mainapp_photoproduct.id_product_id
		
		GROUP BY prod.id, name, price
		ORDER BY prod.name;
		""", basket_list_id
		)
		#  Выполняем запрос и получаем `list`.
		res_db_list: list = list(res_db)
		#  Если в запросе что-то есть.
		if len(res_db_list) > 0:
			# Подсчитываем дубликаты товаров `{<ID_Товара>:<СколькоПовторений>}`.
			count_basket_duplicate = {i: basket_list_id.count(i) for i in basket_list_id}
			# Добавляем колличество дубликатов в модель.
			for _index, _product in enumerate(res_db_list):
				# Количество дубликатов находятся в атрибуте `count_basket_product`
				res_db_list[_index].count_basket_product = count_basket_duplicate[_product.id]
		
		return res_db_list
