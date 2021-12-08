from django.core.validators import MinValueValidator
from django.db import models
# Create your models here.
from django.urls import reverse
from django.utils.text import slugify

from market_dajngo.settings import MEDIA_URL


class CategoryProduct(models.Model):
	objects = None
	name = models.CharField(max_length=255, verbose_name="Категория товара")
	slug = models.SlugField(max_length=255, allow_unicode=True, unique=True, db_index=True,
	                        verbose_name="Слаг категории")
	
	def __str__(self):
		"""
		Для отображение в текстовом виде для админ панели, и консоли.
		"""
		return str(self.name)
	
	class Meta:
		"""
		Вспомогательный класс для админ панели.
		"""
		verbose_name = "Категория товара"  # Имя таблицы в единственном числе
		verbose_name_plural = "Категории товаров"  # Имя таблицы во множественном числе
		ordering = ["pk", ]  # Сортировать записи по указанным столбцам (можно указывать несколько столбцов)


class Product(models.Model):
	objects = None
	name = models.CharField(max_length=255, verbose_name="Имя товара")
	price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Цена")
	is_publish = models.BooleanField(verbose_name="Опубликованное")
	
	# Слишком опасно позволить удалить все товары если удалить категория.
	id_category_product = models.ForeignKey(CategoryProduct, on_delete=models.PROTECT, verbose_name="Имя категории")
	
	time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
	time_update = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
	
	# array_path_photo = ['UrlФото1','UrlФото2','UrlФото3']
	
	def __str__(self):
		"""
		Для отображение в текстовом виде для админ панели, и консоли.
		"""
		return f"{self.id_category_product}<{self.name}"
	
	def get_absolute_url(self):
		"""
		Для получения ссылки записи в Html и отображение в админ панели.
		"""
		return reverse("detail_product", kwargs={"pk": self.pk})
	
	# @staticmethod
	# def unit_produce_with_photo(queryset: RawQuerySet) -> dict[int, models.Model]:
	# 	"""
	# 	Обьеденить товар с фотографиями
	#
	# 	:param queryset: `SELECT id_prod as id, name, price, is_publish, path_photo FROM ...`
	# 	"""
	# 	# Получаем объекты с фотографиями и записываем их в словарь.
	# 	dict_obj: dict[int, Product] = {}
	# 	for _x in queryset:
	# 		_x.path_photo = PhotoProduct.get_absolute_url(img=_x.path_photo)
	# 		if not _x.id in dict_obj:
	# 			_x.path_photo = [_x.path_photo]
	# 			dict_obj[_x.id] = _x
	# 		else:
	# 			dict_obj[_x.id].path_photo.append(_x.path_photo)
	# 	return dict_obj
	
	class Meta:
		"""
		Вспомогательный класс для админ панели.
		"""
		verbose_name = "Товар"  # Имя таблицы в единственном числе
		verbose_name_plural = "Товары"  # Имя таблицы во множественном числе
		ordering = ["pk", ]  # Сортировать записи по указанным столбцам (можно указывать несколько столбцов)


def user_directory_path(instance, filename):
	"""
	Функция, которая будет сохранять файлы по своему пути

	instance =  Это экземпляр вашей модель
	filename = Имя файла
	"""
	# Это путь `MEDIA_ROOT/user_{0}/{1}/{2}`
	return 'user_{0}/{1}/{2}'.format(instance.__class__.__name__, slugify(instance.id_product.name), filename)


class PhotoProduct(models.Model):
	objects = None
	id_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="ID товара")
	path_photo = models.ImageField(upload_to=user_directory_path, max_length=600, verbose_name="Изображения")
	
	def __str__(self):
		"""
		Для отображение в текстовом виде для админ панели, и консоли.
		"""
		return f"{self.id_product}:>{self.path_photo}"
	
	def get_absolute_url(self):
		"""
		Для получения ссылки записи в Html и отображение в админ панели.
		"""
		return f"{MEDIA_URL}{self.path_photo}"
	
	class Meta:
		"""
		Вспомогательный класс для админ панели.
		"""
		verbose_name = "Фото продукта"  # Имя таблицы в единственном числе
		verbose_name_plural = "Фотки продукта"  # Имя таблицы во множественном числе
		ordering = ["pk", ]  # Сортировать записи по указанным столбцам (можно указывать несколько столбцов)
