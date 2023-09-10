from django.urls import path
from .views import organizer, Speaker, event, count_speaker

urlpatterns = [
    path("organizer/", organizer, name="organizer"),
    path("speaker/", Speaker, name="speaker"),
    path("event/", event, name="event"),
    path("count_speaker/", count_speaker, name="count_speaker"),
    # path("temp-payment/", temp_payment, name="temp_payment"),
]
