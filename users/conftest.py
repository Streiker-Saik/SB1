import pytest

from .models import User


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def user():
    return User.objects.create(email="user1@example")
