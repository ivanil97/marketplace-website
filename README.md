# Интернет-магазин MEGANO
***
![Megano_main_page](/django_marketplace/common_static/img/megano_main_screen.png)
## Структура проекта
### Приложения
- adminpanel - административные настройки сайта 
- cart - добавление товаров в корзину и создание заказов
- comparisons - сравнение товаров
- core - основной каталог проекта
- orders - оплата и отслеживание заказов покупателя.
- products - товары, категории, характеристики
- users - личный кабинет, пользователи и продавцы


### Служебные файлы и директории
- fixtures - фикстуры с тестовыми данными
- import - папка для импортируемых данных
- locale - локализация текстовых строк
- mediafiles - загружамые медиа-файлы
- staticfiles - статические файлы для веб-приложения
- templates - шаблоны веб-страниц
- nginx - конфигурация Nginx
- .env.template - шаблон переменных окружения
- docker-compose.yaml - настройки docker-compose для продакшн
- Dockerfile - описание образа Docker
- poetry.* - настройки зависимостей проекта
- start_prod.sh - стартовый скрипт при запуске контейнера Docker

***

## Установка и запуск проекта

Склонировать проект:

```
git clone https://gitlab.skillbox.ru/pythondjango_team42/django_diploma.git
```
В репозитории хранится файл .env.template. Надо на его основе создать и заполнить файл .env 

Если необходимо загрузить тестовые данные, то в файле .env требуется указать:
```
LOAD_FIXTURES=1
```
При загрузке тестовых данных создается три пользователя:

| E-mail             | Пароль           | Категория     |
|--------------------|------------------|---------------|
| andr73@list.ru     | admin            | superuser     |
| seller@seller.ru   | sellerpassword   | Продавец      |
| buyer@buyer.ru     | buyerpassword    | Покупатель    |
**
### Для работы сервиса оплаты необходимо:
- Войти/зарегестрироваться на сервисе "ЮКасса" по ссылке
```
https://yookassa.ru/yooid/signin/step/login?origin=Checkout&returnUrl=https%3A%2F%2Fyookassa.ru%2Fmy%2Fprofile
```
- Создать свой интернет магазин, сдедуя инструкциям ЮКассы
- Перейти по ссылке
```
https://yookassa.ru/my/shop-settings
```
- Из поля "shopId" скопировать id своего магазана
- Перейти по ссылке
```
https://yookassa.ru/my/merchant/integration/api-keys
```
- Из поля "Секретный ключ" скопировать секретный ключ своего магазина
- Перейти по ссылке
```
https://yookassa.ru/my/merchant/integration/http-notifications
```
- Если выключены какие-либо уведомления - включить
- В поле "URL для уведомлений" ввести, где "example.com" пример доменного имени. 
```
https://example.com/payment/notification_url/
```
- В файл .env добавить скопированные "shopId" и "Секретный ключ" в соответсвующие поля
***
Перед запуском проекта необходимо собрать контейнер командой:
```
docker compose build
```

Запуск проекта: 
```
docker compose up -d
```
***
