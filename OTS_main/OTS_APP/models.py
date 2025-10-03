from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# ----------------------------
# Users table
# ----------------------------
class User(AbstractUser):
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
# ----------------------------
# Administrative Users
# ----------------------------
class Manager(User):
    total_tickets_sold = models.IntegerField()
    num_current_events = models.IntegerField()
    num_past_events = models.IntegerField()
    total_income = models.FloatField()

# ----------------------------
# Customers
# ----------------------------
# class Customers(User):

# ----------------------------
# Events table
# ----------------------------
class Event(models.Model):
    event_title = models.CharField(max_length=100)
    event_subtitle = models.CharField(max_length=200)
    event_date = models.DateField()
    event_created = models.DateTimeField(auto_now_add=True)
    event_time = models.TimeField()
    event_price = models.FloatField()
    event_location = models.CharField(max_length=200)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.event_title} ({self.event_date})"
    
# ----------------------------
# Bookings table
# ----------------------------
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    seats_booked = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.name} booked {self.seats_booked} seats for {self.event.event_name}"
