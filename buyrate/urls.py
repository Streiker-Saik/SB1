from django.urls import path

from buyrate.apps import BuyrateConfig
from buyrate.views import (AdCreateAPIView, AdDestroyAPIView, AdRetrieveAPIView, AdsListAPIView, AdUpdateAPIView,
                           AllReviewsListAPIView, ReviewCreateAPIView, ReviewDestroyAPIView, ReviewRetrieveAPIView,
                           ReviewsListAPIView, ReviewUpdateAPIView)

app_name = BuyrateConfig.name

urlpatterns = [
    # CRUD Ad
    path("ads/", AdsListAPIView.as_view(), name="ads"),
    path("ads/create/", AdCreateAPIView.as_view(), name="ad-create"),
    path("ads/<int:pk>/", AdRetrieveAPIView.as_view(), name="ad-detail"),
    path("ads/<int:pk>/update/", AdUpdateAPIView.as_view(), name="ad-update"),
    path("ads/<int:pk>/delete/", AdDestroyAPIView.as_view(), name="ad-delete"),
    # CRUD Review
    path("ads/<int:ad_id>/reviews/", ReviewsListAPIView.as_view(), name="ad-reviews"),
    path("ads/<int:ad_id>/reviews/create/", ReviewCreateAPIView.as_view(), name="review-create"),
    path("ads/<int:ad_id>/reviews/<int:id>/", ReviewRetrieveAPIView.as_view(), name="review-detail"),
    path("ads/<int:ad_id>/reviews/<int:id>/update/", ReviewUpdateAPIView.as_view(), name="review-update"),
    path("ads/<int:ad_id>/reviews/<int:id>/delete/", ReviewDestroyAPIView.as_view(), name="review-delete"),
    # All Review
    path("reviews/", AllReviewsListAPIView.as_view(), name="all-reviews"),
]
