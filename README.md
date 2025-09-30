# Доска объявлений
### Направление: Backend
Теги: CORS, DRF, Django, Git, JWT, ORM, OpenApi_Docs, PEP8, Permissions, PostgresSQL, Readme, 
Serialiers, Test, Viewset/Generic, Auth, Docker, Docker-Compose, Filter
Критерий: pytest

## Содержание:
- [Проверить версию Python](#проверить-версию-python)
- [Установка Poetry](#установка-poetry)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Запуск тестов](#запуск-тестов)
- [Кастомные команды](#кастомные-команды)
- [Структура проекта](#структура-проекта)
- [Приложение buyrate](#приложение-buyrate)
  - [Admin buyrate](#admin-buyrate)
  - [Models buyrate](#models-buyrate)
  - [Paginators buyrate](#paginators-bayrate)
  - [Permissions buyrate](#permissions-bayrate)
  - [Serializers buyrate](#serializers-bayrate)
  - [Urls buyrate](#urls-buyrate)
  - [Views buyrate](#views-buyrate)
- [Приложение users](#приложение-users)
  - [Admin users](#admin-users)
  - [Models users](#models-users)
  - [Serializers user](#serializers-users)
  - [Services users](#services-users)
  - [Tasks users](#tasks-users)
  - [Urls user](#urls-users)
  - [Views user](#views-users)


## Проверить версию Python:

Убедитесь, что у вас установлен Python (версия 3.x). Вы можете проверить установленную версию Python, выполнив команду:
```
python --version
```

[<- на начало](#содержание)


## Установка Poetry:
- Если у вас еще не установлен Poetry, вы можете установить его, выполнив следующую команду
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
- Проверить Poetry добавлен в ваш PATH.
    ```bash
    poetry --version
    ```

[<- на начало](#содержание)


## Установка:
- Клонируйте репозиторий:
    ```bash
    git clone git@github.com:Streiker-Saik/SB1.git
    ```
- Перейдите в директорию проекта:
    ```
    cd SB1
    ```
### При использовании PIP:
- Активируйте виртуальное окружение
    ```
    python -m venv <имя_вашего окружения>
    <имя_вашего_окружения>\Scripts\activate
    ```
- Установите зависимости
    ```bash
    pip install -r requirements.txt
    ```
### При использование POETRY:
- Активируйте виртуальное окружение
    ```bash
    poetry shell
    ```
- Установите необходимые зависимости:
    ```bash
    poetry install
    ```
- Зайдите в файл .env.example и следуйте инструкция

[<- на начало](#содержание)

---
## Запуск проекта:
### Контейнерная сборка:
- Запустите Docker
- Выполните команду в терминале проекта:
  ```bash
  docker-compose up -d --build --force-recreate
  ```
### Локально:
- Redis запустить
- Запуск обработчика очереди (worker)
  - Linux/Mac
    ```bash
    celery -A config worker -l INFO
    ```
  - Windows
    ```bash
    celery -A config worker -l INFO -P eventlet
    ```
- Чтобы запустить сервер разработки, выполните следующую команду:
  ```bash
  python manage.py runserver
  ```

[<- на начало](#содержание)

---
## Запуск тестов:
- При использовании PIP:
  ```bash
  pytest --cov
  ```
- При использовании Poetry:
  ```bash
  poetry run pytest --cov
  ```

[<- на начало](#содержание)

---
## Кастомные команды
### csu
Команда для создания суперпользователя по ключам email, password.
Если не указано, то: email='admin@example.com', password='admin'.
```bash
python manage.py csu
```
или
```
python manage.py csu --email ввести_адрес_почты --password ввести_пароль
```

[<- на начало](#содержание)

---
## Структура проекта:
```
SB1/
├── config/
|   ├── __init__.py
|   ├── asgi.py
|   ├── celery.py # настройка Celery
|   ├── settings.py # настройки проекта
|   ├── urls.py # маршрутизация проета
|   └── wsgi.py
├── buyrate/ # приложение объявлений и отзывов
|   ├── migrations/ # пакет миграции моделей
|   |   └── ...
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── paginators.py # пагинация страниц
|   ├── permissions.py # кастомные права доступа
|   ├── serializaters.py # сериализаторы
|   ├── tests.py 
|   ├── urls.py # маршрутизация приложения
|   └── views.py # конструктор контроллеров
├── users/ # приложение аутефикации
|   ├── migrations/ # пакет миграции моделей
|   |   └── ...
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── permissions.py # права доступа
|   ├── seriazers.py # сериализаторы приложения
|   ├── services.py # сервис приложения
|   ├── tasks.py # отложенные задачи
|   ├── tests.py 
|   ├── urls.py # маршрутизация приложения
|   └── views.py # конструктор контроллеров
├── .env
├── .flake8 # настройка для flake8
├── .gitignore
├── conftest.py # фикстуры для тестов
├── poetry.lock
├── pypproject.toml # зависимости для poetry
├── pytest.ini # настройки для pytest
├── README.md
└── requirements.txt # зависимости для pip
```

[<- на начало](#содержание)

---
# Приложение buyrate:
## Admin buyrate:
### AdAdmin:
Класс для работы администратора с объявлениями
- Атрибуты:
  - ordering - сортировка по дате и времени создания по убыванию
  - list_filter - фильтрация по автору
  - list_display - выводит на экран: название, цена, автор, время и дата создания
  - search_fields - поиск по: назван
### ReviewAdmin:
Класс для работы администратора с отзывами
- Атрибуты:
  - ordering - сортировка по дате и времени создания по убыванию
  - list_filter - фильтрация по автору, объявлению
  - list_display - выводит на экран: автор, объявление, дата и время создания
  - search_fields - поиск по: объявлению

[<- на начало](#содержание)

---
## Models buyrate:
### Ad:
Представление объявления
- Атрибуты:
  - title(str): Название товара 
  - price(int): Цена товара 
  - description(str): Описание товара 
  - author(ForeignKey): Пользователь, который создал объявление
  - created_at(datetime): Время и дата создания объявления.
### Review:
Представление отзыва
- Атрибуты:
  - text(str): Текст отзыва
  - author(ForeignKey): Пользователь, который оставил отзыв
  - ad(ForeignKey): Объявление, под которым оставлен отзыв
  - created_at(datetime): Время и дата создания отзыва.

[<- на начало](#содержание)

---
## Paginators bayrate:
### BuyRatePaginator:
Пагинатор для приложения buyrate  
К-во элементов 4 (максимум 4) на странице

[<- на начало](#содержание)

---
## Permissions bayrate:
### IsAuthor:
Право автора. Доступ, если автор объекта.
### IsAdmin:
Право администратора. Доступ, если пользователь с ролью администратора.

[<- на начало](#содержание)

---
## Serializers bayrate:
### AdSerializers:
Сериализатор для модели Ad.
Отображаются все поля.
### AdCreateSerializers:
Сериализатор для создания модели Ad.
Исключены поля: автор, дата и время создания
### ReviewSerializers:
Сериализатор для модели Review.
Отображаются все поля.
### ReviewCreateSerializers:
Сериализатор для создания модели Review.
Исключены поля: автор, дата и время создания, объявление

[<- на начало](#содержание)

---
## Urls buyrate:
- Список объявлений (доступны методы: **GET**)
  http://127.0.0.1:8000/ads/
  - Фильтрации  
    http://127.0.0.1:8000/users/payments/?title=(title)
    - title - это полное название товара
  - Поиск  
    http://127.0.0.1:8000/users/payments/?search=(title)
    - title - это частичное совпадение в названии товара
- Создание объявления (доступны методы: **POST**)
  http://127.0.0.1:8000/ads/create/
- Получение одного объявления (доступны методы: **GET**)
  http://127.0.0.1:8000/ads/(pk)/
  - pk - это, целое число PrimaryKey, ID объявления
- Редактирование объявления (доступны методы: **PUT/PATH**)
  http://127.0.0.1:8000/ads/(pk)/update/
  - pk - это, целое число PrimaryKey, ID объявления
- Удаление объявления (доступны методы: **DELETE**)
  http://127.0.0.1:8000/ads/(pk)/delete/
  - pk - это, целое число PrimaryKey, ID объявления
- Список отзывов объявления (доступны методы: **GET**)
  http://127.0.0.1:8000/ads/(ad_id)/reviews/
  - ad_id - это, целое число PrimaryKey, ID объявления
  - id - это, целое число PrimaryKey, ID отзыва
- Получение одного объявления (доступны методы: **GET**)
  http://127.0.0.1:8000/ads/(ad_id)/reviews/(pk)/
  - ad_id - это, целое число PrimaryKey, ID объявления
  - pk - это, целое число PrimaryKey, ID отзыва
- Редактирование объявления (доступны методы: **PUT/PATH**)
  http://127.0.0.1:8000/ads/(ad_id)/reviews/(pk)/update/
  - ad_id - это, целое число PrimaryKey, ID объявления
  - pk - это, целое число PrimaryKey, ID отзыва
- Удаление объявления (доступны методы: **DELETE**)
  http://127.0.0.1:8000/ads/(ad_id)/reviews/(pk)/delete/
  - ad_id - это, целое число PrimaryKey, ID объявления
  - pk - это, целое число PrimaryKey, ID отзыва

- Список всех отзывов (доступны методы: **GET**)  
  http://127.0.0.1:8000/reviews/

[<- на начало](#содержание)

---
## Views buyrate:
### Ad
- #### AdsListAPIView:
  Представление для получения списка всех объявлений (GET)
  - Доступ:
    - Всем
- #### AdCreateAPIView:
  Представление для создания объявления (POST)
  - Доступ:
    - авторизованный пользователь
    - Методы:
      - perform_create(self, serializer) -> None:  
      Сохраняет объявление с текущим пользователем как автором.
- #### AdRetrieveAPIView:
  Представление для получения объявления по идентификатору (GET)
  - Доступ:
    - авторизованный пользователь
- #### AdUpdateAPIView:
  Представление для обновления объявления по идентификатору (PUT/PATH)
  - Доступ:
    - автор
    - администратор
- #### AdCreateAPIView:
  Представление для удаления объявления по идентификатору (DELETE)
  - Доступ:
    - автор
    - администратор
### Reviews
- #### AllReviewsListAPIView:
  Представление для получения списка всех отзывов(GET)
  - Доступ:
    - авторизованный пользователь
- #### BaseReviewByAdAPIView:
  Базовый класс представления отзыва от объявления
- #### ReviewsListAPIView:
  Представление для получения списка отзывов конкретного объявления (GET)
  - Доступ:
    - авторизованный пользователь
- #### ReviewCreateAPIView:
  Представление для создания отзыва (POST)
  - Доступ:
    - авторизованный пользователь
  - Методы:
    - perform_create(self, serializer) -> None:  
    Сохраняет отзыв с текущим пользователем как автором и устанавливает ad_id
- #### ReviewRetrieveAPIView:
  Представление для получения отзыва по идентификатору (GET)
  - Доступ:
    - авторизованный пользователь
- #### ReviewUpdateAPIView:
  Представление для обновления отзыва по идентификатору (PUT/PATH)
  - Доступ:
    - автор
    - администратор
- #### ReviewDestroyAPIView:
  Представление для удаления отзыва по идентификатору (DELETE)
  - Доступ:
    - автор
    - администратор

[<- на начало](#содержание)

---
# Приложение users:
## Admin users:
### CustomUserAdmin:
Класс для работы администратора с пользователями
- Атрибуты:
  - ordering - сортировка по email
  - list_filter - фильтрация активный пользователь или нет, по роли
  - exclude - исключит поле пароля
  - list_display - выводит на экран: email, имя, фамилия, роль, сотрудник, активный
  - search_fields - поиск по: email

[<- на начало](#содержание)

---
## Models users:
### User:
Представление пользователя.
- Атрибуты:
  - username: Логин **отключен**
  - email(str): Уникальный email
  - phone(str): Номер телефона
  - role(str): Роль пользователя: user, admin
  - image(ImageField): Аватар (изображение)
  - token(str): Токен для восстановления пароля

[<- на начало](#содержание)

---
## Serializers users:
### UserCreateSerializer:
Сериализатор для создания модели Users.
- Показывает поля:
  - id(int): Уникальный идентификатор пользователя
  - email(str): Почта пользователя
  - first_name(str): Имя пользователя
  - last_name(str): Фамилия пользователя
  - phone(str): Номер телефона пользователя
  - role(str): Роль пользователя: user, admin

[<- на начало](#содержание)

---
## Services users:
### UserService:
Сервисное класс для работы с пользователями
- Методы:
  - send_email(subject: str, message: str, user_emails: list) -> None:  
  Отправка письма на email.

[<- на начало](#содержание)

---
## Tasks users:
### send_password_recovery_email:
Отправляет электронное письмо для восстановления пароля.
- Атрибуты:
  - email: Email пользователя
  - uidb64: Зашифрованный id пользователя
  - token: Токен для сброса пароля

[<- на начало](#содержание)

---
## Urls users:
- Получение токена пользователя (доступны методы: **POST**)  
  http://127.0.0.1:8000/users/token/
- Обновление токена пользователя (доступны методы: **POST**)  
  http://127.0.0.1:8000/users/token/refresh/
- Создание пользователя (доступны методы: **POST**)
  http://127.0.0.1:8000/users/register/
- Запрос на обновление пароля (доступны методы: **POST**)
  http://127.0.0.1:8000/users/reset_password/
- Подтверждение изменения пароля(доступны методы: **POST**)
  http://127.0.0.1:8000/users/reset_password_confirm/

[<- на начало](#содержание)

---
## Views users:
### UserCreateAPIView:
Представление для создания пользователя (POST)  
- Доступ: 
  - Всем
- Методы:
  - perform_create(self, serializer) -> None:  
  Сохраняет нового пользователя и устанавливает его активным.
### UserResetPassword:
Представление для запроса на сброс пароля пользователя (POST)  
- Доступ: 
  - Всем
- Методы:
  - post(self, request: Request) -> Response:  
  Запрос сброса пароля для пользователя.
### UserResetPasswordConfirm:
Представление для подтверждения сброса пароля пользователя (POST)  
- Доступ: 
  - Всем
- Методы:
  - post(self, request: Request) -> Response:  
  Подтверждает сброс пароля для пользователя.

[<- на начало](#содержание)

---