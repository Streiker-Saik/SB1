from django.db import models

from config import settings


class Ad(models.Model):
    """
    Представление объявления
    Атрибуты:
        title(str): Название товара
        price(int): Цена товара
        description(str): Описание товара
        author(ForeignKey): Пользователь, который создал объявление
        created_at(datetime): Время и дата создания объявления.
    """

    title = models.CharField(max_length=255, verbose_name="Название", help_text="Введите название товара")
    price = models.PositiveIntegerField(verbose_name="Цена", help_text="Введите цену товара")
    description = models.TextField(verbose_name="Описание", help_text="Введите описание товара")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name="ads",
        verbose_name="Создатель объявления",
        help_text="Введите ID автора объявления",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время и дата создания", help_text="Автоматическое время создания"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "объявление"
        verbose_name_plural = "объявления"


class Review(models.Model):
    """
    Представление отзыва
    Атрибуты:
        text(str): Текст отзыва
        author(ForeignKey): Пользователь, который оставил отзыв
        ad(ForeignKey): Объявление, под которым оставлен отзыв
        created_at(datetime): Время и дата создания отзыва.
    """

    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name="reviews",
        verbose_name="Создатель отзыва",
        help_text="Введите ID автора отзыва",
    )
    ad = models.ForeignKey(
        Ad, models.CASCADE, related_name="reviews", verbose_name="Объявление", help_text="Введите ID объявления"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время и дата создания", help_text="Автоматическое время создания"
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
