from django.db import models
from accounts.models import CustomUser
import uuid


# Create your models here.
class Organizer(models.Model):
    INDUSTRY_TYPE_CHOICES = (
        ("technology", "Technology"),
        ("finance", "Finance"),
        ("healthcare", "Healthcare"),
        ("education", "Education"),
        ("other", "Other"),
    )
    organizer_id = models.AutoField(primary_key=True)
    organizer_name = models.CharField(max_length=100)
    industry_type = models.CharField(max_length=50, choices=INDUSTRY_TYPE_CHOICES)
    organizer_email = models.EmailField(max_length=100)
    organizer_mobile_no = models.CharField(max_length=20)
    organizer_image = models.URLField(max_length=200, blank=True, null=True)
    contact_person_name = models.CharField(max_length=100)
    contact_person_email = models.EmailField(max_length=100)
    contact_person_mobile_no = models.CharField(max_length=10)
    contact_person_designation = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    def __str__(self):
        return self.organizer_name


class Events(models.Model):
    EVENT_TYPE_CHOICES = (
        ("conference", "Conference"),
        ("forum", "Forum"),
        ("exhibition", "Exhibition"),
        ("education", "Education"),
        ("other", "Other"),
    )
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=50, choices=EVENT_TYPE_CHOICES, null=True, blank=True
    )
    event_agenda = models.CharField(max_length=200)
    event_description = models.CharField(max_length=200)
    event_image = models.URLField(max_length=200, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    number_of_panels = models.IntegerField(blank=True, null=True)
    venue_link = models.URLField(max_length=200)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    total_seats = models.IntegerField()
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    user = models.ManyToManyField(CustomUser)

    def __str__(self):
        return str(self.event_name)


class Panels(models.Model):
    panel_id = models.AutoField(primary_key=True)
    panel_no = models.IntegerField(null=True, blank=True)
    panel_name = models.CharField(max_length=200)
    panel_description = models.CharField(max_length=200)
    panel_topic = models.CharField(max_length=200)
    panel_image = models.URLField(max_length=200, blank=True, null=True)
    panel_start_time = models.DateTimeField()
    panel_end_time = models.DateTimeField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    events = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.panel_name


class TicketInfo(models.Model):
    TICKET_TYPE_CHOICES = (
        ("with_food", "With Food"),
        ("without_food", "Without Food"),
        ("online", "Online"),
        ("guest", "GUEST"),
    )
    ticket_id = models.AutoField(primary_key=True)
    ticket_type = models.CharField(max_length=100, choices=TICKET_TYPE_CHOICES)
    ticket_type1 = models.CharField(
        max_length=100, blank=True, null=True
    )  # for future use
    ticket_price = models.IntegerField()
    ticket_description = models.CharField(max_length=100, blank=True, null=True)
    tickets_available = models.IntegerField()
    tickets_sold = models.IntegerField(blank=True, null=True)
    tickets_scanned = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    events = models.ForeignKey(Events, on_delete=models.CASCADE)

    def __str__(self):
        return (
            self.events.event_name
            + " , "
            + self.ticket_type
            + " , "
            + str(self.ticket_price)
        )


class Sponsors(models.Model):
    SPONSOR_TYPE_CHOICES = (
        ("sponsors", "Sponsors"),
        ("main_sponsors", "Main Sponsors"),
        ("partners", "Partners"),
        ("media_partners", "Media Partners"),
    )
    sponsor_id = models.AutoField(primary_key=True)
    sponsor_type = models.CharField(max_length=50, choices=SPONSOR_TYPE_CHOICES)
    sponsor_name = models.CharField(max_length=100)
    sponsor_image = models.URLField(max_length=200, blank=True, null=True)
    sponsor_description = models.CharField(max_length=100)
    sponsor_email = models.EmailField(max_length=100)
    sponsor_mobile_no = models.CharField(max_length=10)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    events = models.ForeignKey(Events, on_delete=models.CASCADE)

    def __str__(self):
        return self.sponsor_name


class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    notification_title = models.CharField(max_length=100)
    notification_content = models.TextField(max_length=200)
    notification_image = models.URLField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notification_title + " " + str(self.notification_date)


# class Bookings(models.Model):
#     booking_id = models.AutoField(primary_key=True)
#     ticket_id = models.ForeignKey(TicketInfo, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
#     booking_date = models.DateTimeField(auto_now_add=True)
#     booking_status = models.CharField(max_length=100)
#     payment_id = models.CharField(max_length=100, default=uuid.uuid4())
#     # total_scanned = models.AutoField()
#     # total_booked = models.AutoField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)


# class Payment(models.Model):
#     payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
#     payment_type = models.CharField(max_length=100)
#     payment_status = models.CharField(max_length=100)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     payment_amount = models.IntegerField()
#     booking_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
