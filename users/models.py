from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Представление пользователя
    Атрибуты:
        username: Логин отключен
        email(str): Уникальный email
        phone(str): Номер телефона
        role(str): Рол пользователя: user, admin
        image(ImageField): Аватар (изображение)
    """
    ROLE_CHOICES = [("user", "пользователь"), ("admin", "администратор")]
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите уникальный адрес электронной почты"
    )
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона", help_text="Введите свой номер телефона"
    )
    role = models.CharField(max_length=5, default="user", choices=ROLE_CHOICES, verbose_name="Роль пользователя")
    image = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите изображение аватара"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
