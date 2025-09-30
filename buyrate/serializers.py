from rest_framework import serializers

from buyrate.models import Ad, Review


class AdSerializers(serializers.ModelSerializer):
    """
    Сериализатор для модели Ad.
    Отображаются все поля.
    """

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializers(serializers.ModelSerializer):
    """
    Сериализатор для создания модели Ad.
    Исключены поля: автор, дата и время создания
    """

    class Meta:
        model = Ad
        exclude = ["author", "created_at"]


class ReviewSerializers(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.
    Отображаются все поля.
    """

    class Meta:
        model = Review
        fields = "__all__"


class ReviewCreateSerializers(serializers.ModelSerializer):
    """
    Сериализатор для создания модели Review.
    Исключены поля: автор, дата и время создания, объявление
    """

    class Meta:
        model = Review
        exclude = ["author", "created_at", "ad"]
