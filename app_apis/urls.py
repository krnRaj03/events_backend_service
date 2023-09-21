from django.urls import path
from .views import fetchAllEventsView, fetchEventByIdView, fetchSpeakersByEventIdView

urlpatterns = [
    path("fetch-all-events/", fetchAllEventsView.as_view(), name="fetchAllEventsView"),
    path(
        "fetch-event/<int:event_id>",
        fetchEventByIdView.as_view(),
        name="fetchEventByIdView",
    ),
    path(
        "fetch-speakers/<int:event_id>",
        fetchSpeakersByEventIdView.as_view(),
        name="fetchSpeakersByEventIdView",
    ),
]
