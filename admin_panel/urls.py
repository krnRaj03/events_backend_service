from django.urls import path
from .views import ( Speaker,
                 count_speaker,admin_login,
                 admin_home,add_events,admin_stastics)

urlpatterns = [
    path("speaker/", Speaker, name="speaker"),
    path("count_speaker/", count_speaker, name="count_speaker"),
    path("admin-login/", admin_login, name="admin_login"),
    path("admin-home/", admin_home, name="admin_home"),
    path("add-events/", add_events, name="add_events"),
    path("admin-stats/", admin_stastics, name="admin_stastics"),
]
