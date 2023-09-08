from django.contrib import admin
from .models import Organizer, Events, TicketInfo, Sponsors, Notifications

# Register your models here.

admin.site.register(Organizer)
admin.site.register(Events)
admin.site.register(TicketInfo)
admin.site.register(Sponsors)
admin.site.register(Notifications)
