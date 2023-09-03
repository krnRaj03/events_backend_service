# Django imports
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import random

# Project/app level imports
from .models import CustomUser
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    UserProfileSerializer,
    SendResetPasswordEmailSerializer,
    ResetPasswordSerializer,
    UserProfileUpdateSerializer,
)
from utilities import (
    password_check,
    send_email_with_sendgrid,
    get_tokens_for_user,
    send_forget_password_email,
)
from .renderers import UserRenderer
from admin_panel.models import Events, TicketInfo, Sponsors


# Create your views here.
class SignupView(APIView):
    """Render JSON response for signup view"""

    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if password_check(request.data.get("password")) == False:
                return Response(
                    {
                        "message": "Password must have atleast 8 charecters! Please use atleast 1 UC, 1 symbol & 1 digit"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user = serializer.save()
                # Generate and save OTP
                otp = str(random.randint(100000, 999999))
                user.email_otp = otp
                # Send OTP to user's email address
                send_email_with_sendgrid(user.email, "Your OTP is {}".format(otp))
                user.save()

                return Response(
                    {"message": "User registered successfully!OTP sent to email"},
                    status=status.HTTP_201_CREATED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        otp = request.data.get("otp")
        try:
            user = CustomUser.objects.get(email_otp=otp)
            user.is_verified = True
            user.status = "signup_done"
            user.save()
            return Response({"message": "Email verified."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid OTP! Please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    """Render JSON response for login view"""

    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        # try:
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "message": "Login successful!",
                        "status": user.status,
                        "role": user.role,
                        "is_user": user.is_user,
                        "token": token,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Email or password is not valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class SendResetPasswordEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    "message": "Password Reset link sent successfully! Please check your email."
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = ResetPasswordSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Password reset successful!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileUpdateView(APIView):
    """This view is used to update user profile i.e basic info, address, etc."""

    """We can put "required fields" check in react here while booking ticket"""

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserProfileUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            user.status = "profile_updated"
            user.save()
            return Response(
                {"message": "Profile updated successfully!"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
