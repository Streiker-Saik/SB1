from django.contrib import admin

from .models import Ad, Review


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Класс для работы администратора с объявлениями
    Атрибуты:
        ordering - сортировка по дате и времени создания по убыванию
        list_filter - фильтрация по автору, дате и времени создания
        list_display - выводит на экран: название, цена, автор, время и дата создания
        search_fields - поиск по: названию
    """

    ordering = ("-created_at",)
    list_filter = ("author", "created_at")
    list_display = (
        "title",
        "price",
        "author",
        "created_at",
    )
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Класс для работы администратора с отзывами
    Атрибуты:
        ordering - сортировка по дате и времени создания по убыванию
        list_filter - фильтрация по автору, объявлению, дате и времени создания
        list_display - выводит на экран: автор, объявление, дата и время создания
        search_fields - поиск по: объявлению
    """

    ordering = ("-created_at",)
    list_filter = ("author", "ad", "created_at")
    list_display = (
        "author",
        "ad",
        "created_at",
    )
    search_fields = ("ad",)
