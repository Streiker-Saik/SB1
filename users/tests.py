import secrets
from unittest.mock import MagicMock, patch

import pytest
from django.core.management import call_command
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes
from rest_framework import status
from rest_framework.test import APIClient

from config import settings
from users.models import User
from users.services import UserService
from users.tasks import send_password_recovery_email


@pytest.mark.django_db
def test_user_str(user: User):
    """Тестирование строкового представление модели пользователя"""
    assert str(user) == user.email


@pytest.mark.django_db
def test_create_superuser(capsys: pytest.CaptureFixture) -> None:
    """Тестирование команды созданию суперпользователя по умолчанию"""
    assert not User.objects.exists()
    call_command("csu")
    superuser = User.objects.first()
    assert superuser is not None
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.is_active
    assert superuser.check_password("admin")
    assert User.objects.count() == 1

    captured = capsys.readouterr()
    assert "Суперпользователь admin@example.com создан успешно!" in captured.out


@pytest.mark.django_db
def test_create_superuser_params() -> None:
    """Тестирование создание суперпользователя с параметрами"""
    email = "admin1@example.com"
    assert not User.objects.filter(email=email).exists()
    password = "admin1"
    call_command("csu", "--email", email, "--password", password)
    superuser = User.objects.filter(email=email).first()
    assert superuser is not None
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.is_active
    assert superuser.check_password(password)
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_create_superuser_user_exists(capsys: pytest.CaptureFixture, user: User) -> None:
    """Тестирование создание суперпользователя если пользователь уже существует"""

    call_command("csu", "--email", user.email, "--password", "test")

    captured = capsys.readouterr()
    assert "Суперпользователь с данным email уже существует." in captured.out


@pytest.mark.django_db
def test_create_user(api_client: APIClient) -> None:
    """Тестирование создание пользователя"""
    data = {"email": "test@test.com", "password": "test12345"}
    response = api_client.post(reverse("users:register"), data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        "id": User.objects.get(email=data["email"]).pk,
        "email": "test@test.com",
        "first_name": "",
        "last_name": "",
        "phone": None,
        "role": "user",
    }
    assert User.objects.filter(email="test@test.com").exists()


@pytest.mark.django_db
@patch("users.tasks.send_password_recovery_email.delay")
def test_reset_password(mock_send_email: MagicMock, api_client: APIClient, user: User) -> None:
    """Тестирование запроса восстановления пароля"""
    data = {"email": user.email}

    response = api_client.post(reverse("users:reset_password"), data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"detail": "Ссылка для сброса успешно отправлена"}

    mock_send_email.assert_called_once()


@pytest.mark.django_db
@patch("users.services.send_mail")
def test_send_email(mock_send_mail: MagicMock, user: User) -> None:
    """Тестирование сервисного метода отправки сообщения"""
    subject = "Тестовая тема"
    message = "Тестовый текст"
    user_emails = [user.email]
    UserService.send_email(subject, message, user_emails)
    assert mock_send_mail.call_count == 1
    mock_send_mail.assert_called_once_with(subject, message, settings.DEFAULT_FROM_EMAIL, user_emails)


@pytest.mark.django_db
@patch("users.services.UserService.send_email")
def test_send_password_recovery_email(mock_send_email: MagicMock, user: User) -> None:
    """Тестирование отложенной задачи отправки email пользователю"""
    subject = "Восстановление пароля"
    uidb64 = "AB"
    token = "test_token"
    url = f"{settings.BASE_URL}reset_password_confirm/{uidb64}/{token}"
    send_password_recovery_email(user.email, uidb64, token)
    assert mock_send_email.call_count == 1
    mock_send_email.assert_called_once_with(subject, url, [user.email])


@pytest.mark.django_db
def test_reset_password_empty_email(api_client: APIClient) -> None:
    """Тестирование запроса восстановления пароля, если пользователь не найден"""
    data = {"email": "nonexists@test.com"}

    response = api_client.post(reverse("users:reset_password"), data=data)

    assert not User.objects.filter(email=data["email"]).exists()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"detail": "Пользователь не найден"}


@pytest.mark.django_db
def test_reset_password_confirm(api_client: APIClient, user: User) -> None:
    """Тестирование подтверждение сброса пароля"""

    uid64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = secrets.token_hex(16)
    user.token = token
    user.save()
    password = "new12345"

    data = {"uid": uid64, "token": token, "new_password": password}

    response = api_client.post(reverse("users:reset_password_confirm"), data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"detail": "Пароль успешно изменен"}

    user.refresh_from_db()
    assert user.check_password(password) is True


@pytest.mark.django_db
def test_reset_password_confirm_empty_user(api_client: APIClient) -> None:
    """Тестирование подтверждения сброса пароля, если пользователь не найден"""
    uid64 = urlsafe_base64_encode(force_bytes("9999"))

    data = {"uid": uid64, "token": "test", "new_password": "test"}

    response = api_client.post(reverse("users:reset_password_confirm"), data=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"detail": "Пользователь не найден"}


@pytest.mark.django_db
def test_reset_password_confirm_invalid_token(api_client: APIClient, user: User) -> None:
    """Тестирование подтверждения сброса пароля, если токен не корректный"""
    uid64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
    data = {"uid": uid64, "token": "test", "new_password": "test"}

    response = api_client.post(reverse("users:reset_password_confirm"), data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {"detail": "Токен не корректный"}
