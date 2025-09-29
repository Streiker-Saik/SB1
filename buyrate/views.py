from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from buyrate.models import Ad, Review
from buyrate.paginators import BuyRatePaginator
from buyrate.permissions import IsAdmin, IsAuthor
from buyrate.serializers import AdCreateSerializers, AdSerializers, ReviewCreateSerializers, ReviewSerializers


class AdsListAPIView(ListAPIView):
    """
    Представление для получения списка всех объявлений (GET)
    """

    queryset = Ad.objects.order_by("-create_at")
    pagination_class = BuyRatePaginator
    permission_classes = (AllowAny,)
    serializer_class = AdSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["title"]
    search_fields = ["title"]



class AdCreateAPIView(CreateAPIView):
    """
    Представление для создания объявления (POST)
    Методы:
        perform_create(self, serializer) -> None:
            Сохраняет объявление с текущим пользователем как автором.
    """

    serializer_class = AdCreateSerializers

    @swagger_auto_schema(operation_id="ad_create")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        """Сохраняет объявление с текущим пользователем как автором."""
        serializer.save(author=self.request.user)


class AdRetrieveAPIView(RetrieveAPIView):
    """Представление для получения объявления по идентификатору (GET)"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializers

    @swagger_auto_schema(operation_id="ad_read")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdUpdateAPIView(UpdateAPIView):
    """Представление для обновления объявления по идентификатору (PUT/PATH)"""

    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializers
    permission_classes = (
        IsAuthenticated,
        IsAuthor | IsAdmin,
    )

    @swagger_auto_schema(operation_description="Полное обновление объявления", operation_id="ad_update")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Частичное обновление объявления", operation_id="ad_partial_update")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class AdDestroyAPIView(DestroyAPIView):
    """Представление для удаления объявления по идентификатору (DELETE)"""

    queryset = Ad.objects.all()
    permission_classes = (IsAuthenticated, IsAuthor | IsAdmin)

    @swagger_auto_schema(operation_id="ad_delete")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AllReviewsListAPIView(ListAPIView):
    """Представление для получения списка всех отзывов(GET)"""

    queryset = Review.objects.all().order_by("-create_at")
    pagination_class = BuyRatePaginator
    serializer_class = ReviewSerializers

    @swagger_auto_schema(operation_id="all_review_list")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BaseReviewByAdAPIView:
    """Базовый класс представления отзыва от объявления"""

    queryset = Review.objects.all()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()

        ad_id = self.kwargs.get("ad_id")

        if ad_id is None:
            return Review.objects.none()

        if not Ad.objects.filter(id=ad_id).exists():
            raise NotFound("Объявление с данным ID не найдено.")

        queryset = Review.objects.filter(ad_id=ad_id)
        return queryset


class ReviewsListAPIView(ListAPIView, BaseReviewByAdAPIView):
    """Представление для получения списка отзывов конкретного объявления (GET)"""

    pagination_class = BuyRatePaginator
    serializer_class = ReviewSerializers

    @swagger_auto_schema(
        operation_id="ad_reviews_list",
        manual_parameters=[
            openapi.Parameter(
                "ad_id",
                openapi.IN_PATH,
                description="ID объявления, связанного с отзывом",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ReviewCreateAPIView(CreateAPIView):
    """
    Представление для создания отзыва (POST)
    Методы:
        perform_create(self, serializer) -> None:
            Сохраняет отзыв с текущим пользователем как автором и устанавливает ad_id
    """

    serializer_class = ReviewCreateSerializers

    @swagger_auto_schema(
        operation_id="review_create",
        manual_parameters=[
            openapi.Parameter(
                "ad_id",
                openapi.IN_PATH,
                description="ID объявления, связанного с отзывом",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        """Сохраняет объявление с текущим пользователем как автором и устанавливает ad_id"""
        ad_id = self.kwargs.get("ad_id")
        serializer.save(author=self.request.user, ad_id=ad_id)


class ReviewRetrieveAPIView(RetrieveAPIView, BaseReviewByAdAPIView):
    """Представление для получения отзыва по идентификатору (GET)"""

    serializer_class = ReviewSerializers

    @swagger_auto_schema(
        operation_id="review_read",
        manual_parameters=[
            openapi.Parameter(
                "ad_id",
                openapi.IN_PATH,
                description="ID объявления, связанного с отзывом",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID отзыва, который нужно получить",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ReviewUpdateAPIView(UpdateAPIView, BaseReviewByAdAPIView):
    """Представление для обновления отзыва по идентификатору (PUT/PATH)"""

    serializer_class = ReviewCreateSerializers
    permission_classes = (
        IsAuthenticated,
        IsAuthor | IsAdmin,
    )

    @swagger_auto_schema(
        operation_description="Полное обновление отзыва",
        operation_id="review_update",
        manual_parameters=[
            openapi.Parameter(
                "ad_id",
                openapi.IN_PATH,
                description="ID объявления, связанного с отзывом",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID отзыва, который нужно изменить",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление отзыва",
        operation_id="review_partial_update",
        manual_parameters=[
            openapi.Parameter(
                "ad_id",
                openapi.IN_PATH,
                description="ID объявления, связанного с отзывом",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID отзыва, который нужно изменит",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ReviewDestroyAPIView(DestroyAPIView, BaseReviewByAdAPIView):
    """Представление для удаления отзыва по идентификатору (DELETE)"""

    serializer_class = ReviewSerializers
    permission_classes = (
        IsAuthenticated,
        IsAuthor | IsAdmin,
    )

    @swagger_auto_schema(
        operation_id="review_delete",
        manual_parameters=[
            openapi.Parameter(
                "ad_id",
                openapi.IN_PATH,
                description="ID объявления, связанного с отзывом",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID отзыва, который нужно удалить",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
