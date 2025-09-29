import pytest
from rest_framework.test import APIClient

from buyrate.models import Ad, Review
from users.models import User


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_api_client(api_client: APIClient, user: User) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_api_client(api_client: APIClient, admin: User) -> APIClient:
    api_client.force_authenticate(user=admin)
    return api_client


@pytest.fixture
def user() -> User:
    return User.objects.create(email="user1@example.com")


@pytest.fixture
def user_two() -> User:
    return User.objects.create(email="user2@example.com")


@pytest.fixture
def admin() -> User:
    return User.objects.create(email="user_admin@example.com", role="admin")


# title, price, description, author, created_at
@pytest.fixture
def ad_one(user: User):
    return Ad.objects.create(
        title="Смартфон Samsung Galaxy S21",
        price=60000,
        description="Продаю новый смартфон Samsung Galaxy S21. Цвет: черный, 128 ГБ.",
        author=user,
    )


@pytest.fixture
def ad_two(user_two: User):
    return Ad.objects.create(
        title="Ноутбук Acer Aspire 5",
        price=45000,
        description="Продаю ноутбук Acer Aspire 5 в отличном состоянии. 8 ГБ ОЗУ, 256 ГБ SSD.",
        author=user_two,
    )


# text, author, ad, created_at
@pytest.fixture
def review_one(user_two: User, ad_one: Ad) -> Review:
    return Review.objects.create(text="Отличный смартфон! Очень доволен покупкой.", author=user_two, ad=ad_one)


@pytest.fixture
def review_two(user: User, ad_two: Ad) -> Review:
    return Review.objects.create(text="Ноутбук работает без нареканий. Рекомендую!", author=user, ad=ad_two)
