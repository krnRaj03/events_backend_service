from django.urls import path

from .views import (
    SignupView,
    VerifyOTPView,
    LoginView,
    UserProfileView,
    SendResetPasswordEmailView,
    ResetPasswordView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
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
]
