from rest_framework import serializers
from admin_panel.models import Events
from accounts.models import CustomUser


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        exclude = ("date_created", "date_updated")


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
