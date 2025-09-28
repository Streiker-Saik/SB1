from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from buyrate.models import Ad
from buyrate.paginators import BuyRatePaginator
from buyrate.permissions import IsAuthor, IsAdmin
from buyrate.serializers import AdSerializers, AdCreateSerializers, ReviewSerializers


class AdsListAPIView(ListAPIView):
    """
    Представление для получения списка всех объявлений (GET)
    """

    queryset = Ad.objects.order_by("-create_at")
    pagination_class = BuyRatePaginator
    permission_classes = (AllowAny,)
    serializer_class = AdSerializers


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
        serializer.save(owner=self.request.user)


class AdRetrieveAPIView(RetrieveAPIView):
    """Представление для получения объявления по идентификатору (GET)"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializers
    permission_classes = (IsAuthenticated, IsAuthor, IsAdmin,)

    @swagger_auto_schema(operation_id="ad_read")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdUpdateAPIView(UpdateAPIView):
    """Представление для обновления объявления по идентификатору (PUT/PATH)"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializers
    permission_classes = (IsAuthenticated, IsAuthor, IsAdmin,)

    @swagger_auto_schema(operation_description="Полное обновление объявления", operation_id="ad_update")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Частичное обновление объявления", operation_id="ad_partial_update")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class AdDestroyAPIView(DestroyAPIView):
    """Представление для удаления объявления по идентификатору (DELETE)"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializers
    permission_classes = (IsAuthenticated, IsAuthor, IsAdmin,)

    @swagger_auto_schema(operation_id="ad_delete")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
