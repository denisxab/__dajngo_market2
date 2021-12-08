$(document).ready(function () {

// Когда документ загружен
	
	
	$('.AddProductInBasket').submit(function () {
			// Объект для отправки на сервер
			const dataVar = {
				flag: 'AddProductInBasket',
				// Id товара
				id_product: $(this).attr('id_product'),
				// Необходимый csrf токен
				csrfmiddlewaretoken: $(this).attr('csrfmiddlewaretoken'),
			};
			console.log(dataVar);
			// Отправляем `ajax` запрос
			$.ajax({
				// Тело сообщения
				method: "POST", // Берем метод из формы
				url: UrlBasketServer, // Берем url из формы
				data: dataVar, // Данные на сервер
				
				// Если при отправке возникли ошибки
				error: function (response) {
					const exceptionVar = "Ошибка отправки" + response
					alert(exceptionVar);
					console.log(exceptionVar)
				}
			}).done(function (msg) { // Получаем ответ от сервера, и обрабатываем его.
				console.log(msg);
				// Изменяем колличество товаров в корзине
				UpdateBasket(msg);
			});
			// Остановить перезагрузку страницы
			return false;
		}
	);
	
	
	$('.DeleteProductInBasket').submit(function () {
			let id_product = $(this).attr('id_product');
			
			// Объект для отправки на сервер
			const dataVar = {
				flag: 'DeleteProductInBasket',
				// Id товара
				id_product: id_product,
				// Необходимый csrf токен
				csrfmiddlewaretoken: $(this).attr('csrfmiddlewaretoken'),
			};
			
			console.log(dataVar);
			// Отправляем `ajax` запрос
			$.ajax({
				// Тело сообщения
				method: "POST", // Берем метод из формы
				url: UrlBasketServer, // Берем url из формы
				data: dataVar, // Данные на сервер
				
				// Если при отправке возникли ошибки
				error: function (response) {
					const exceptionVar = "Ошибка отправки" + response
					alert(exceptionVar);
					console.log(exceptionVar)
				}
			}).done(function (msg) { // Получаем ответ от сервера, и обрабатываем его.
				console.log(msg);
				DeleteProductFromBasket(id_product);
				// Изменяем колличество товаров в корзине
				UpdateBasket(msg);
				
			});
			// Остановить перезагрузку страницы
			return false;
		}
	);
	
	
	function GetBasketFromServer() {
		// Отправляем `ajax` запрос
		$.ajax({
			// Тело сообщения
			method: "GET", // Берем метод из формы
			url: UrlBasketServer, // Берем url из формы
			
			// Если при отправке возникли ошибки
			error: function (response) {
				const exceptionVar = "Ошибка отправки" + response;
				alert(exceptionVar);
				console.log(exceptionVar);
			}
		}).done(function (msg) { // Получаем ответ от сервера, и обрабатываем его.
			console.log(msg);
			UpdateBasket(msg);
		})
	}
	
	
	function UpdateBasket(msg) {
		// Получить
		const basket = msg['basket']['list_select_product']['length']
		if (basket != null) {
			// Изменяем колличество товаров в корзине
			$("#BasketInfo").html(msg['basket']['list_select_product']['length']);
		} else {
			// Изменяем колличество товаров в корзине
			$("#BasketInfo").html('0');
		}
	}
	
	function DeleteProductFromBasket(id_product) {
		const list_box_product = $(`#${id_product}-span`)
		if (list_box_product.html() - 0 > 1) {
			list_box_product.html(list_box_product.html() - 1)
		} else {
			$(`#${id_product}`).remove();
		}
		
	}
	
	GetBasketFromServer();
})
