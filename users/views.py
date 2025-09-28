import secrets

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserCreateSerializer
from users.tasks import send_password_recovery_email


class UserCreateAPIView(CreateAPIView):
    """
    Представление для создания пользователя (POST)
    Методы:
        perform_create(self, serializer) -> None:
            Сохраняет нового пользователя и устанавливает его активным.
    """

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer) -> None:
        """Сохраняет нового пользователя и устанавливает его активным."""
        serializer.save(is_active=True)


class UserResetPassword(APIView):
    """
    Представление для запроса на сброс пароля пользователя (POST)
    Методы:
        post(self, request: Request) -> Response:
            Запрос сброса пароля для пользователя.
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_id="reset_password",
        manual_parameters=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email пользователя"),
            },
            required=["email"],
        ),
        responses={
            200: openapi.Response("Ссылка для сброса успешно отправлена"),
            404: openapi.Response("Пользователь не найден"),
        },
    )
    def post(self, request: Request) -> Response:
        """
        Запрос сброса пароля доля пользователя
        Параметры запроса:
            {
                email (str): Email пользователя
            }
        :param request: HTTP запрос, содержащий информацию для запроса сброса пароля.
        :return: Ответ с сообщением о результате операции.
        """
        email = request.data.get("email")
        try:
            user = get_object_or_404(User, email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = secrets.token_hex(16)
            user.token = token
            user.save()
            send_password_recovery_email.delay(email, uidb64, token)
            return Response({"detail": "Ссылка для сброса успешно отправлена"}, status=status.HTTP_200_OK)
        except Http404:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class UserResetPasswordConfirm(APIView):
    """
    Представление для подтверждения сброса пароля пользователя (POST)
    Методы:
        post(self, request: Request) -> Response:
            Подтверждает сброс пароля для пользователя.
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_id="reset_password_confirm",
        manual_parameters=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "uid": openapi.Schema(type=openapi.TYPE_STRING, description="ID пользователя, зашифрованное"),
                "token": openapi.Schema(type=openapi.TYPE_STRING, description="Token"),
                "new_password": openapi.Schema(type=openapi.TYPE_STRING, description="Новый пароль"),
            },
            required=["uid", "token", "new_password"],
        ),
        responses={
            200: openapi.Response("Пароль успешно изменен"),
            403: openapi.Response("Токен не корректный"),
            404: openapi.Response("Пользователь не найден"),
        },
    )
    def post(self, request: Request) -> Response:
        """
        Подтверждает сброс пароля на основе предоставленных данных.
        Параметры запроса:
            {
                uid (str): Зашифрованный ID пользователя
                token (str): Токен для сброса пароля
                new_password (str): Новый пароль для пользователя
            }
        :param request: HTTP запрос, содержащий информацию для сброса пароля.
        :return: Ответ с сообщением о результате операции.
        """
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
            if user.token != token:
                return Response({"detail": "Токен не корректный"}, status=status.HTTP_403_FORBIDDEN)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
        except Http404:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
