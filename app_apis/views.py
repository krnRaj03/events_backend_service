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
