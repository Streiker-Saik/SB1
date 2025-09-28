from django.urls import path

from buyrate.apps import BuyrateConfig
from buyrate.views import AdsListAPIView, AdCreateAPIView, AdRetrieveAPIView, AdUpdateAPIView, AdDestroyAPIView

app_name = BuyrateConfig.name

urlpatterns = [
    # CRUD Ad
    path("ads/", AdsListAPIView.as_view(), name="ads"),
    path("ads/create/", AdCreateAPIView.as_view(), name="ad-create"),
    path("ads/<int:pk>/", AdRetrieveAPIView.as_view(), name="ad-detail"),
    path("ads/<int:pk>/update/", AdUpdateAPIView.as_view(), name="ad-update"),
    path("ads/<int:pk>/delete/", AdDestroyAPIView.as_view(), name="ad-delete"),
    # CRUD Review
]
