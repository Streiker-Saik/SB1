from django.urls import path
from users.apps import UsersConfig
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

from users.views import UserCreateAPIView, UserResetPassword, UserResetPasswordConfirm

app_name = UsersConfig.name

urlpatterns = [
    # Token
    path("token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    # User
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("reset_password/", UserResetPassword.as_view(), name="reset_password"),
    path("reset_password_confirm/", UserResetPasswordConfirm.as_view(), name="reset_password_confirm"),
]