from django.core.mail import send_mail

from config import settings


class UserService:
    """
    Сервисное класс для работы с пользователями
    Методы:
        send_email(subject: str, message: str, user_emails: list) -> None:
            Отправка письма на email.
    """

    @staticmethod
    def send_email(subject: str, message: str, user_emails: list) -> None:
        """
        Отправка письма на email
        :param subject: Тема сообщения
        :param message: Текст сообщения
        :param user_emails: Список почты для отправки
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = user_emails
        send_mail(subject, message, from_email, recipient_list)
