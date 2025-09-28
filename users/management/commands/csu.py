from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания суперпользователя по ключам email, password и chat_id.
    Если не указано, то: email='admin@example.com', password='admin', chat_id=1.
    Методы:
        add_arguments(self, parser):
            Добавляет аргументы команды: email, password, chat_id.
        handle(self, *args, **options) -> None:
            Обрабатывает команду для создания суперпользователя.
        custom_create_superuser(email: str, password: str, chat_id: int) -> None:
            Кастомное создание суперпользователя
    """

    help = "Создание суперпользователя с email, password и chat_id."

    def add_arguments(self, parser):
        """Добавляет аргументы команды: email, password, chat_id."""
        parser.add_argument("--email", type=str, default="admin@example.com", help="Email для входя суперпользователя")
        parser.add_argument("--password", type=str, default="admin", help="Пароль для входя суперпользователя")
        parser.add_argument("--chat_id", type=int, default=1, help="ID телеграмма")

    def handle(self, *args, **options) -> None:
        """Обрабатывает команду для создания суперпользователя."""
        email = options["email"]
        password = options["password"]
        chat_id = options["chat_id"]
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("Суперпользователь с данным email уже существует."))
        else:
            self.custom_create_superuser(email, password, chat_id)
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь {email} создан успешно!"))

    @staticmethod
    def custom_create_superuser(email: str, password: str, chat_id: int) -> None:
        """Кастомное создание суперпользователя"""
        user = User.objects.create(email=email, chat_id=chat_id)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
