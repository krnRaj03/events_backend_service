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
    organizer_mobile_no = models.CharField(max_length=10)
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
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organizer_name


class Events(models.Model):
    events_id = models.AutoField(primary_key=True)
    events_name = models.CharField(max_length=100)
    events_description = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    total_seats = models.IntegerField()
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    user = models.ManyToManyField(CustomUser)

    def __str__(self):
        return str(self.events_name)


class TicketInfo(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_type = models.CharField(max_length=100)
    ticket_price = models.IntegerField()
    ticket_description = models.CharField(max_length=100)
    total_tickets = models.IntegerField()
    total_tickets_sold = models.IntegerField()
    total_tickets_scanned = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    events_id = models.ForeignKey(Events, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_type


class Sponsors:
    sponsor_id = models.AutoField(primary_key=True)
    sponsor_name = models.CharField(max_length=100)
    sponsor_description = models.CharField(max_length=100)
    sponsor_email = models.EmailField(max_length=100)
    sponsor_mobile_no = models.CharField(max_length=10)
    sponsor_address_line1 = models.CharField(max_length=100)
    sponsor_address_line2 = models.CharField(max_length=100)
    sponsor_city = models.CharField(max_length=100)
    sponsor_state = models.CharField(max_length=100)
    sponsor_country = models.CharField(max_length=100)
    sponsor_pincode = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    events_id = models.ForeignKey(Events, on_delete=models.CASCADE)

    def __str__(self):
        return self.sponsor_name


# class Speakers(models.Model):
#     speaker_id = models.AutoField(primary_key=True)
#     speaker_name = models.CharField(max_length=100)
#     speaker_description = models.CharField(max_length=100)
#     speaker_email = models.EmailField(max_length=100)
#     speaker_mobile_no = models.CharField(max_length=10)
#     speaker_address_line1 = models.CharField(max_length=100)
#     speaker_address_line2 = models.CharField(max_length=100)
#     speaker_city = models.CharField(max_length=100)
#     speaker_state = models.CharField(max_length=100)
#     speaker_country = models.CharField(max_length=100)
#     speaker_pincode = models.CharField(max_length=100)
#     speaker_image = models.URLField(max_length=200, blank=True, null=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
#     events = models.ForeignKey(Events, on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.speaker_name) + " || " + str(self.events.events_name)


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
