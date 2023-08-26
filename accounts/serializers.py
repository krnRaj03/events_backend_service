from rest_framework import serializers
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import CustomUser, Address
from utilities import send_forget_password_email

# create a serializer class for the user model


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address  # Replace with your actual Address model
        fields = "__all__"


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password", "confirm_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password_errors": "Password & confirm password didn't match."}
            )
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            validated_data["email"], validated_data["password"]
        )


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Foregin key serializer for user address"""

    user_address = AddressSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "user_image",
            "user_address",
        ]


class SendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=250)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(email=attrs["email"])
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:3000/reset-password/" + uid + "/" + token
            send_forget_password_email(
                user.email, f"Please click this link to Reset your password! {link}"
            )
            return attrs

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"errors": "Email not found! Please enter a valid email address."}
            )


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        try:
          uid=self.context.get("uid")
          token=self.context.get("token")
          if attrs["password"] != attrs["confirm_password"]:
              raise serializers.ValidationError(
                  {"password_errors": "Password & confirm password didn't match."}
              )
          id=smart_str(urlsafe_base64_decode(uid))
          user=CustomUser.objects.get(id=id)
          if not PasswordResetTokenGenerator().check_token(user, token):
              raise serializers.ValidationError(
                  {"errors": "Invalid token! Please request a new one."}
              )
          user.set_password(attrs["password"])
          user.save()
          return attrs
        
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError(
                {"error": "Invalid token! Please request a new one."}
            )
            
