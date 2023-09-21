# Django imports
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import datetime
from django.http import JsonResponse
from django.utils import timezone


# Project/app level imports
from accounts.models import CustomUser
from admin_panel.models import Events
from .serializers import EventsSerializer, CustomUserSerializer

from utilities import (
    password_check,
    send_email_sendgrid,
    get_tokens_for_user,
    create_order,
)
from accounts.renderers import UserRenderer
from admin_panel.models import Events, TicketInfo, Sponsors


# Fethch all events
class fetchAllEventsView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Events.objects.all()
        # Serialize the events data using the serializer
        serializer = EventsSerializer(events, many=True)
        # Return the serialized data as JSON response
        return Response(serializer.data)


# Fetch event by ID
class fetchEventByIdView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Events.objects.get(event_id=event_id)
            serializer = EventsSerializer(event, many=False)
            sd = serializer.data["start_date"]

            print(sd)
            return Response(serializer.data)
        except:
            return Response(
                {"message": "Event with this ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Ferch speakers by event ID
class fetchSpeakersByEventIdView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def get(self, request, event_id, format=None):
        try:
            event = Events.objects.get(event_id=event_id)
        except Events.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Fetch the users related to the event
        related_users = event.user.all()
        user_data = [
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_pic": user.user_image,
                "job_title": user.job_title,
                "work_place": user.work_place,
                "linkedin_url": user.linkedin_url,
                "twitter_url": user.twitter_url,
                "facebook_url": user.facebook_url,
                "instagram_url": user.instagram_url,
                "bio": user.bio,
            }
            for user in related_users
        ]

        return Response({"users": user_data}, status=status.HTTP_200_OK)
