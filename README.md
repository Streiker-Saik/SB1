# Доска объявлений
### Направление: Backend
Теги: CORS, DRF, Django, Git, JWT, ORM, OpenApi_Docs, PEP8, Permissions, PostgresSQL, Readme, 
Serialiers, Test, Viewset/Generic, Auth, Docker, Docker-Compose, Filter

## Содержание:
- [Приложение users](#приложение-users)
  - [Admin users](#admin-users)
  - [Models users](#models-users)
    - [User](#user)


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

[<- на начало](#содержание)

---