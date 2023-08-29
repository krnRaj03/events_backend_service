from django.db import models
from accounts.models import CustomUser, Address
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
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)


class Events(models.Model):
    events_id = models.AutoField(primary_key=True)
    events_name = models.CharField(max_length=100)
    events_description = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    total_seats = models.IntegerField()
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    organizer_id = models.ForeignKey(Organizer, on_delete=models.CASCADE)


class TicketInfo:
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    ticket_type = models.CharField(max_length=100)
    ticket_price = models.IntegerField()
    ticket_description = models.CharField(max_length=100)
    total_tickets = models.IntegerField()
    total_tickets_sold = models.IntegerField()
    total_tickets_scanned = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    events_id = models.ForeignKey(Events, on_delete=models.CASCADE)


class Bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    ticket_id = models.ForeignKey(TicketInfo, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, default=uuid.uuid4())
    total_scanned = models.AutoField()
    total_booked = models.AutoField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.IntegerField()
    booking_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
