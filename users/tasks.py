from celery import shared_task

from config import settings
from users.services import UserService


@shared_task
def send_password_recovery_email(email: str, uidb64: str, token: str) -> None:
    """
    Отправляет электронное письмо для восстановления пароля.
    :param email: Email пользователя
    :param uidb64: Зашифрованный id пользователя
    :param token: Токен для сброса пароля
    """

    url = f"{settings.BASE_URL}reset_password_confirm/{uidb64}/{token}"
    subject = "Восстановление пароля"
    message = url
    recipient_list = [email]
    UserService.send_email(subject, message, recipient_list)
