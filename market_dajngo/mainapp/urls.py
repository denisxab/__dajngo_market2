from django.urls import path

from mainapp.views import ListProduct, DetailProduct, Basket, BasketServer

urlpatterns = [
		path('', ListProduct.as_view(), name='main_lenta_product'),
		path('product/<int:pk>', DetailProduct.as_view(), name="detail_product"),
		path('basket/server', BasketServer.as_view(), name="basket_server"),
		path('basket', Basket.as_view(), name="basket"),
]
