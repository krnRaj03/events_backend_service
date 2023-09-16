from django.urls import path
from .views import (
    count_speaker,
    admin_login,
    admin_home,
    add_events,
    admin_stastics,
    delete_event,
    edit_event,
)

urlpatterns = [
    path("count_speaker/", count_speaker, name="count_speaker"),
    path("admin-login/", admin_login, name="admin_login"),
    path("admin-home/", admin_home, name="admin_home"),
    path("add-events/", add_events, name="add_events"),
    path("admin-stats/", admin_stastics, name="admin_stastics"),
    path("edit-event/<int:event_id>", edit_event, name="edit_event"),
    path("delete-event/<int:event_id>", delete_event, name="delete_event"),
]
