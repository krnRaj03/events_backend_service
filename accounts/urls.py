from django.urls import path

from .views import (
    SignupView,
    VerifyOTPView,
    LoginView,
    SendResetPasswordEmailView,
    ResetPasswordView,
    UserProfileView,
    UserProfileUpdateView,
    approve_url,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "send-reset-password-email/",
        SendResetPasswordEmailView.as_view(),
        name="send-rest-password-email",
    ),
    path(
        "reset-password/<uid>/<token>/",
        ResetPasswordView.as_view(),
        name="rest-password",
    ),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path(
        "update-profile/<int:pk>",
        UserProfileUpdateView.as_view(),
        name="update-profile",
    ),
    path(
        "approveURL/",
        approve_url.as_view(),
        name="approve-url",
    ),
]
