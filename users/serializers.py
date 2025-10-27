from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserCreateSerializer(ModelSerializer):
    """
    Сериализатор для создания модели Users.
    Показывает поля:
        id(int): Уникальный идентификатор пользователя
        email(str): Почта пользователя
        first_name(str): Имя пользователя
        last_name(str): Фамилия пользователя
        phone(str): Номер телефона пользователя
        role(str): Роль пользователя: user, admin
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "role", "password")

    def create(self, validated_data):
        """Создает нового пользователя и хэширует его пароль."""
        user = User(**validated_data)
        user.set_password(validated_data.pop("password"))
        user.save()
        return user
