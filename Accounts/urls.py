from django.urls import path
from .views import (
    LoginView,
    UserRegistrationView,
    UserProfileView,
    UserUpdateView,
    LogoutView,
    DepositMoneyView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView, name="logout"),
    path("update/", UserUpdateView.as_view(), name="update_profile"),
    path("deposit-money/", DepositMoneyView.as_view(), name="deposit_money"),
]
