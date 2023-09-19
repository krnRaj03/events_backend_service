from django.urls import path
from .views import (
    admin_login,
    admin_home,
    add_events,
    all_events,
    delete_event,
    edit_event,
    edit_speaker,
    all_speakers,
    all_users,
    all_tickets,
    view_event,
)

urlpatterns = [
    path("admin-login/", admin_login, name="admin_login"),
    path("admin-home/", admin_home, name="admin_home"),
    path("add-events/", add_events, name="add_events"),
    path("all-events/", all_events, name="all_events"),
    path("edit-event/<int:event_id>", edit_event, name="edit_event"),
    path("edit-speaker/<int:speaker_id>", edit_speaker, name="edit_speaker"),
    path("delete-event/<int:event_id>", delete_event, name="delete_event"),
    path("all-speakers/", all_speakers, name="all_speakers"),
    path("all-users/", all_users, name="all_users"),
    path("all-tickets/", all_tickets, name="all_tickets"),
    path("view-event/<int:event_id>", view_event, name="view_event"),
]
