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
        ("buyrate:ad-review-create", {"ad_id": 1}, "post", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:ad-review-detail", {"ad_id": 1, "pk": 1}, "get", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:ad-review-update", {"ad_id": 1, "pk": 1}, "put", status.HTTP_401_UNAUTHORIZED),
        ("buyrate:ad-review-delete", {"ad_id": 1, "pk": 1}, "delete", status.HTTP_401_UNAUTHORIZED),
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
    if ad_two.created_at > ad_one.created_at:
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
def test_partial_update_ad_admin(admin_api_client: APIClient, ad_one: Ad) -> None:
    """Тестирование частичного обновления объявления"""
    data = {"title": "Смартфон Samsung Galaxy S21 Ultra"}
    response = admin_api_client.patch(reverse("buyrate:ad-update", kwargs={"pk": ad_one.pk}), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == ad_one.pk
    assert response.data["title"] == data["title"]
    assert response.data["price"] == ad_one.price


@pytest.mark.django_db
def test_destroy_ad(user_api_client: APIClient, ad_one: Ad) -> None:
    """Тестирование удаления объявления"""
    initial_count = Ad.objects.count()
    response = user_api_client.delete(reverse("buyrate:ad-delete", kwargs={"pk": ad_one.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == initial_count - 1


@pytest.mark.django_db
def test_destroy_ad_not_author(user_api_client: APIClient, ad_two: Ad) -> None:
    """Тестирование запрета удаления чужого объявления"""
    initial_count = Ad.objects.count()
    response = user_api_client.delete(reverse("buyrate:ad-delete", kwargs={"pk": ad_two.pk}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ad.objects.count() == initial_count


@pytest.mark.django_db
def test_destroy_ad_admin(admin_api_client: APIClient, ad_one: Ad) -> None:
    """Тестирование удаления чужого объявления администратором"""
    initial_count = Ad.objects.count()
    response = admin_api_client.delete(reverse("buyrate:ad-delete", kwargs={"pk": ad_one.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == initial_count - 1


@pytest.mark.django_db
def test_list_all_reviews(user_api_client: APIClient, review_one: Review, review_two: Review) -> None:
    """Тестирование получение списка всех отзывов"""
    response = user_api_client.get(reverse("buyrate:all-reviews"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert response.data["next"] is None
    assert response.data["previous"] is None
    assert "results" in response.data
    results = response.data["results"]
    assert len(results) == 2
    if review_two.created_at > review_one.created_at:
        assert results[0]["id"] == review_two.pk
        assert results[1]["id"] == review_one.pk


@pytest.mark.django_db
def test_not_found_ad_id(user_api_client: APIClient):
    """Тестирование обработки несуществующего ad_id"""
    response = user_api_client.get(reverse("buyrate:ad-reviews", kwargs={"ad_id": 0}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Объявление с данным ID не найдено."


@pytest.mark.django_db
def test_list_reviews_by_ad(user_api_client: APIClient, ad_one: Ad, review_one: Review, review_two: Review) -> None:
    """Тестирование получение списка отзывов по объявлению"""
    response = user_api_client.get(reverse("buyrate:ad-reviews", kwargs={"ad_id": ad_one.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["next"] is None
    assert response.data["previous"] is None
    assert "results" in response.data
    results = response.data["results"]
    assert len(results) == 1


@pytest.mark.django_db
def test_create_review_by_ad(user_api_client: APIClient, ad_one: Ad, user: User) -> None:
    """Тестирование создания отзыва по объявлению"""
    initial_count = Review.objects.count()
    data = {"text": "Отличный смартфон! Продавец просто супер."}
    response = user_api_client.post(reverse("buyrate:ad-review-create", kwargs={"ad_id": ad_one.pk}), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == data["text"]
    assert "id" in response.data
    assert Review.objects.count() == initial_count + 1
    review = Review.objects.get(text=data["text"])
    assert review.author == user
    assert review.ad == ad_one


@pytest.mark.django_db
def test_read_review_by_ad(user_api_client: APIClient, ad_one: Ad, review_one: Review) -> None:
    """Тестирование просмотра отзыва по объявлению"""
    response = user_api_client.get(
        reverse("buyrate:ad-review-detail", kwargs={"ad_id": ad_one.pk, "pk": review_one.pk})
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == review_one.pk
    assert response.data["text"] == review_one.text
    assert response.data["ad"] == review_one.ad.id


@pytest.mark.django_db
def test_update_review_by_ad(user_api_client: APIClient, ad_two: Ad, review_two: Review) -> None:
    """Тестирование обновления отзыва по объявлению"""
    data = {
        "text": "Ноутбук бомба. Рекомендую!",
    }
    response = user_api_client.put(
        reverse("buyrate:ad-review-update", kwargs={"ad_id": ad_two.pk, "pk": review_two.pk}), data=data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == review_two.pk
    assert response.data["text"] == data["text"]


@pytest.mark.django_db
def test_partial_update_review_by_ad(user_api_client: APIClient, ad_two: Ad, review_two: Review) -> None:
    """Тестирование частичного обновления отзыва по объявлению"""
    data = {
        "text": "Ноутбук бомба. Рекомендую!",
    }
    response = user_api_client.patch(
        reverse("buyrate:ad-review-update", kwargs={"ad_id": ad_two.pk, "pk": review_two.pk}), data=data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == review_two.pk
    assert response.data["text"] == data["text"]


@pytest.mark.django_db
def test_update_review_by_ad_not_author(user_api_client: APIClient, ad_one: Ad, review_one: Review) -> None:
    """Тестирование запрета изменения чужого отзыва по объявлению"""
    data = {
        "text": "Не понравилось.",
    }
    response = user_api_client.patch(
        reverse("buyrate:ad-review-update", kwargs={"ad_id": ad_one.pk, "pk": review_one.pk}), data=data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_partial_update_review_by_ad_admin(admin_api_client: APIClient, ad_two: Ad, review_two: Review) -> None:
    """Тестирование частичного обновления отзыва по объявлению"""
    data = {
        "text": "Ноутбук замечательный. Рекомендую!",
    }
    response = admin_api_client.patch(
        reverse("buyrate:ad-review-update", kwargs={"ad_id": ad_two.pk, "pk": review_two.pk}), data=data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == review_two.pk
    assert response.data["text"] == data["text"]


@pytest.mark.django_db
def test_destroy_review_by_ad(user_api_client: APIClient, ad_two: Ad, review_two: Review) -> None:
    """Тестирование удаления отзыва"""
    initial_count = Review.objects.count()
    print(initial_count)
    response = user_api_client.delete(
        reverse("buyrate:ad-review-delete", kwargs={"ad_id": ad_two.pk, "pk": review_two.pk})
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == initial_count - 1


@pytest.mark.django_db
def test_destroy_review_by_ad_not_author(user_api_client: APIClient, ad_one: Ad, review_one: Review) -> None:
    """Тестирование запрета удаления чужого отзыва"""
    initial_count = Review.objects.count()
    response = user_api_client.delete(
        reverse("buyrate:ad-review-delete", kwargs={"ad_id": ad_one.pk, "pk": review_one.pk})
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Review.objects.count() == initial_count


@pytest.mark.django_db
def test_destroy_review_by_ad_admin(admin_api_client: APIClient, ad_two: Ad, review_two: Review) -> None:
    """Тестирование удаления чужого отзыва администратором"""
    initial_count = Review.objects.count()
    response = admin_api_client.delete(
        reverse("buyrate:ad-review-delete", kwargs={"ad_id": ad_two.pk, "pk": review_two.pk})
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == initial_count - 1
