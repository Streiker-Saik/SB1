# Доска объявлений
### Направление: Backend
Теги: CORS, DRF, Django, Git, JWT, ORM, OpenApi_Docs, PEP8, Permissions, PostgresSQL, Readme, 
Serialiers, Test, Viewset/Generic, Auth, Docker, Docker-Compose, Filter

## Содержание:
- [Проверить версию Python](#проверить-версию-python)
- [Установка Poetry](#установка-poetry)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Структура проекта](#структура-проекта)
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
pass
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
├── poetry.lock
├── pypproject.toml # зависимости для poetry
├── README.md
└── requirements.txt # зависимости для pip
```

[<- на начало](#содержание)

---
# Приложение users:
## Admin users
### CustomUserAdmin
Класс для работы администратора с пользователями
- Атрибуты:
  - ordering - сортировка по email
  - list_filter - фильтрация активный пользователь или нет, по роли
  - exclude - исключит поле пароля
  - list_display - выводит на экран: email, имя, фамилия, роль, сотрудник, активный
  - search_fields - поиск по: email

[<- на начало](#содержание)

---
## Models users
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
### UserService
Сервисное класс для работы с пользователями
- Методы:
  - send_email(subject: str, message: str, user_emails: list) -> None:  
  Отправка письма на email.

[<- на начало](#содержание)

---
## Tasks users:
### send_password_recovery_email
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