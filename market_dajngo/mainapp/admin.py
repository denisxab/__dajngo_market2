# Register your models here.


from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import *


@admin.register(CategoryProduct)  # Регестрируем модель БД, с классом `admin.ModelAdmin`
class CategoryProductAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")  # Имя столбца которые мы хотим видеть в админ панели
	list_display_links = ("name",)  # Указать имя столбца через которое можно перейти редактированию записи
	search_fields = ("name", "slug")  # Указать по каким столбцам можно делать поиск
	list_editable = ("slug",)  # Столбцы которые можно редактировать не открывая всю запись
	# list_filter = ("name", "slug")  # Столбцы, по которым можно фильтровать записи
	
	prepopulated_fields = {"slug": ("name",)}  # Авто заполнение слага URL на основе столбца
	
	# readonly_fields = (...,)  # Поля которые можно только смотреть, но не редактировать.
	# fields = (...,)  # Порядок отображения полей при редактировании записи
	
	save_on_top = False  # Панель с удаление/созданием записи вверху редактирования запси.


@admin.register(PhotoProduct)  # Регестрируем модель БД, с классом `admin.ModelAdmin`
class PhotoProductAdmin(admin.ModelAdmin):
	list_display = ("id_product", "path_photo")  # Имя столбца которые мы хотим видеть в админ панели
	list_display_links = ("id_product",)  # Указать имя столбца через которое можно перейти редактированию записи
	search_fields = ("id_product", "path_photo")  # Указать по каким столбцам можно делать поиск
	# list_editable = ("")  # Столбцы которые можно редактировать не открывая всю запись
	list_filter = ("id_product",)  # Столбцы, по которым можно фильтровать записи
	# date_hierarchy = ""  # Поля в котром содержится дата создания
	
	# prepopulated_fields = {"slug": ("name",)}  # Авто заполнение слага URL на основе столбца
	# readonly_fields = ("",)  # Поля которые можно только смотреть, но не редактировать.
	# fields = (...,)  # Порядок отображения полей при редактировании записи
	
	save_on_top = False  # Панель с удаление/созданием записи вверху редактирования запси.


class PhotoInline(admin.StackedInline):
	
	def get_html_photo(self, obj):
		"""
		"""
		print(obj)
		tmp = self.model.objects.get(pk=obj.id)
		res = "нет фото"
		if tmp:
			res = mark_safe(f"<img src='{tmp.path_photo.url}'  style='object-fit: contain;' width=150 height=150><br>")
		return res
	
	get_html_photo.short_description = "Изображения"
	readonly_fields = ("get_html_photo",)  # Поля которые можно только смотреть, но не редактировать.
	fields = ("id_product", ("path_photo", "get_html_photo"))
	model = PhotoProduct  # Вторичная модель
	# fk_name = "" # Имя атрибута внешнего ключа
	extra = 1  # Начально количество форм
	max_num = 10  # Максимальное количество форм
	min_num = 1  # Минимально количество форм
	# template = Шаблон таблицы
	can_delete = True  # Можно ли удалять объекты
	show_change_link = False  # Можно ли изменять объекты


def my_validator(var: str):
	return True


class Pto(forms.ModelForm):
	"""
	Пример кастомноый формы
	"""
	
	re = forms.ChoiceField(choices=(
			('chevrolet', 'Chevrolet'),
			('mazda', 'Mazda'),
			('nissan', 'Nissan'),
			('toyota', 'Toyota'),
			('mitsubishi', 'Mitsubishi'),)
			, validators=[my_validator], help_text="Тестовый пример")
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def clean_re(self):
		res = self.cleaned_data["re"]
		return res


@admin.register(Product)  # Регистрируем модель БД, с классом `admin.ModelAdmin`
class ProductAdmin(admin.ModelAdmin):
	
	# def get_html_all_photo(self, obj):
	# 	"""
	# 	Все изображения
	# 	"""
	# 	tmp = PhotoProduct.objects.filter(id_product=obj.id)
	# 	res = "Нет фото"
	# 	if tmp:
	# 		res = ""
	# 		for _x in tmp:
	# 			res += f"<img src='{_x.path_photo.url}'  style='object-fit: contain;' width=150 height=150><br>"
	# 	return mark_safe(res)
	# get_html_all_photo.short_description = "Изображения"  # Имя столбца миниатюрой
	#
	#
	def set_publish(self, request, queryset):
		"""Метод - действие"""
		row_update = queryset.update(is_publish=True)
		# Сообщение в админ панель
		self.message_user(request, f"Записей опубликовано: {row_update}")
	
	# Название в админ панели
	set_publish.short_description = "Опубликовать"
	# Выполнять это действия могу  только пользователи с правами на `редактирования` записи
	set_publish.allowed_permissions = ("change",)
	
	def del_publish(self, request, queryset):
		row_update = queryset.update(is_publish=False)
		self.message_user(request, f"Записей снято с публикации: {row_update}")
	
	# Название в админ панели
	del_publish.short_description = "Снять с публикации"
	# Выполнять это действия могу  только пользователи с правами на `редактирования` записи
	del_publish.allowed_permissions = ("change",)
	
	def get_html_first_photo(self, obj):
		"""
		Миниатюра
		"""
		tmp = PhotoProduct.objects.filter(id_product=obj.id)
		res = "Нет фото"
		if tmp:
			res = f"<img src='{tmp.first().path_photo.url}'  style='object-fit: contain;' width=150 height=150><br>"
		return mark_safe(res)
	
	get_html_first_photo.short_description = "Миниатюра"
	
	def show_image(self, obj):
		return format_html("<h1>1</h1>")
	
	#
	
	list_display = (
			"name", "price", "get_html_first_photo", "is_publish",
			"id_category_product", 'show_image')  # Имя столбца которые мы хотим видеть в админ панели
	list_display_links = ("name",)  # Указать имя столбца через которое можно перейти редактированию записи
	search_fields = ("name", "id_category_product")  # Указать по каким столбцам можно делать поиск
	list_editable = ("price",)  # Столбцы которые можно редактировать не открывая всю запись
	list_filter = ("price", "id_category_product")  # Столбцы, по которым можно фильтровать записи
	
	save_as = True
	inlines = [PhotoInline]
	save_on_top = True  # Панель с удаление/созданием записи вверху редактирования запси.
	
	actions = ["set_publish", "del_publish"]  # Регистрируем действия
	
	date_hierarchy = "time_create"  # Поля, в котором содержится дата создания
	
	# prepopulated_fields = {"slug": ("name",)}  # Авто заполнение слага URL на основе столбца
	readonly_fields = ("time_create", "time_update")  # Поля которые можно только смотреть, но не редактировать.
	
	# fields = (...,)  # Порядок отображения полей при редактировании записи
	
	autocomplete_fields = ("id_category_product",)  # Добавить Поиск по указзаным полям ForeignKey/ManyToManyField
	# raw_id_fields = ["id_category_product"]
	form = Pto
	
	def save_model(self, request, obj, form, change):
		# Метод вызывается при нажатии кнопки сохранить
		super().save_model(request, obj, form, change)
	
	def get_form(self, request, obj=None, **kwargs):
		"""
		Вызывается при получении формы для редактирования записи
		"""
		form = super().get_form(request, obj, **kwargs)
		form.base_fields["id_category_product"].empty_label = "Без категории"
		return form
