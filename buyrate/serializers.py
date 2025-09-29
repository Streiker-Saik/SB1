from rest_framework import serializers

from buyrate.models import Ad, Review


class AdSerializers(serializers.ModelSerializer):
    """
    Сериализатоор для модели Ad.
    Отображаются все поля.
    """

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializers(serializers.ModelSerializer):
    """
    Сериализатоор для модели Ad.
    Исключены поля: автор, дата и время создания
    """

    class Meta:
        model = Ad
        exclude = ["author", "create_at"]


class ReviewSerializers(serializers.ModelSerializer):
    """
    Сериализатоор для модели Review.
    Отображаются все поля.
    """

    class Meta:
        model = Review
        fields = "__all__"


class ReviewCreateSerializers(serializers.ModelSerializer):
    """
    Сериализатоор для модели Review.
    Исключены поля: автор, дата и время создания, объявление
    """

    class Meta:
        model = Review
        exclude = ["author", "create_at", "ad"]
