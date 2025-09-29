import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from buyrate.models import Ad, Review
from users.models import User


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_name, url_kwargs, method, expected_status",
    [
        ("buyrate:ad-create", None, "post", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:ad-detail", {"pk": 1}, "get", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:ad-update", {"pk": 1}, "put", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:ad-delete", {"pk": 1}, "delete", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:ad-reviews", {"ad_id": 1}, "get", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:review-create", {"ad_id": 1}, "post", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:review-detail", {"ad_id": 1, "id": 1}, "get", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:review-update", {"ad_id": 1, "id": 1}, "put", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:review-delete", {"ad_id": 1, "id": 1}, "delete", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:all-reviews", None, "get", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_not_authenticated(
    api_client: APIClient, url_name: str, url_kwargs: dict, method: str, expected_status: int
) -> None:
    """Тестирование доступа не авторизованного пользователя"""
    if url_kwargs:
        url = reverse(url_name, kwargs=url_kwargs)
    else:
        url = reverse(url_name)
    response = getattr(api_client, method)(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_ad_str(ad_one: Ad) -> None:
    """Тестирование строкового представление модели объявления"""
    assert str(ad_one) == ad_one.title


@pytest.mark.django_db
def test_review_str(review_one: Review) -> None:
    """Тестирование строкового представление модели отзывов"""
    assert str(review_one) == review_one.text


@pytest.mark.django_db
def test_list_ads(api_client: APIClient, ad_one: Ad, ad_two: Ad) -> None:
    """Тестирование получение списка всех объявлений"""
    response = api_client.get(reverse("buyrate:ads"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert response.data["next"] is None
    assert response.data["previous"] is None
    assert "results" in response.data
    results = response.data["results"]
    assert len(results) == 2
    if ad_two.create_at > ad_one.create_at:
        assert results[0]["id"] == ad_two.pk
        assert results[1]["id"] == ad_one.pk


@pytest.mark.django_db
def test_filters_list_ads(api_client: APIClient, ad_one: Ad, ad_two: Ad) -> None:
    """Тестирование фильтрации объявлений по названию"""
    response = api_client.get(f"{reverse('buyrate:ads')}?title=Смартфон Samsung Galaxy S21")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_search_ads_by_title(api_client: APIClient, ad_one: Ad, ad_two: Ad) -> None:
    """Тестирование поиск объявлений по названию"""
    response = api_client.get(f"{reverse('buyrate:ads')}?search=Смартфон")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_create_ad(user_api_client: APIClient, user: User) -> None:
    """Тестирование создания объявления"""
    initial_count = Ad.objects.count()
    data = {
        "title": "Электровелосипед",
        "price": 35000,
        "description": "Продаю электровелосипед, пробег 100 км, состояние нового.",
    }
    response = user_api_client.post(reverse("buyrate:ad-create"), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == data["title"]
    assert response.data["price"] == data["price"]
    assert response.data["description"] == data["description"]
    assert "id" in response.data
    assert Ad.objects.count() == initial_count + 1
    ad = Ad.objects.get(title=data["title"])
    assert ad.author == user


@pytest.mark.django_db
def test_read_ad(user_api_client: APIClient, ad_one: Ad) -> None:
    """Тестирование просмотра объявления"""
    response = user_api_client.get(reverse("buyrate:ad-detail", kwargs={"pk": ad_one.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == ad_one.pk
    assert response.data["title"] == ad_one.title
    assert response.data["price"] == ad_one.price
    assert response.data["description"] == ad_one.description


@pytest.mark.django_db
def test_update_ad(user_api_client: APIClient, ad_one: Ad) -> None:
    """Тестирование обновления объявления"""
    data = {
        "title": "Смартфон Samsung Galaxy S21 Ultra",
        "price": 100000,
        "description": "Продаю новый смартфон Samsung Galaxy S21 Ultra. Цвет: черный, 128 ГБ.",
    }
    response = user_api_client.put(reverse("buyrate:ad-update", kwargs={"pk": ad_one.pk}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == ad_one.pk
    assert response.data["title"] == data["title"]
    assert response.data["price"] == data["price"]
    assert response.data["description"] == data["description"]


@pytest.mark.django_db
def test_partial_update_ad(user_api_client: APIClient, ad_one: Ad) -> None:
    """Тестирование частичного обновления объявления"""
    data = {"title": "Смартфон Samsung Galaxy S21 Ultra"}
    response = user_api_client.patch(reverse("buyrate:ad-update", kwargs={"pk": ad_one.pk}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == ad_one.pk
    assert response.data["title"] == data["title"]
    assert response.data["price"] == ad_one.price


@pytest.mark.django_db
def test_update_ad_not_author(user_api_client: APIClient, ad_two: Ad) -> None:
    """Тестирование запрета изменения чужого объявления"""
    data = {"title": "Смартфон Samsung Galaxy S21 Ultra"}
    response = user_api_client.patch(reverse("buyrate:ad-update", kwargs={"pk": ad_two.pk}), data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_destroy_ad(user_api_client: APIClient, ad_one: Ad) -> None:
    """Тестирование удаления объявления"""
    response = user_api_client.delete(reverse("buyrate:ad-delete", kwargs={"pk": ad_one.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == 0


@pytest.mark.django_db
def test_destroy_ad_not_author(user_api_client: APIClient, ad_two: Ad) -> None:
    """Тестирование запрета удаления чужого объявления"""
    response = user_api_client.delete(reverse("buyrate:ad-delete", kwargs={"pk": ad_two.pk}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ad.objects.count() == 1
