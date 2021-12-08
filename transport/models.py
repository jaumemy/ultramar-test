from django.db import models
from uuid import uuid4



class Booking(models.Model):
    booking_number = models.UUIDField(unique=True, primary_key=True, default=uuid4)
    loading_port = models.CharField(max_length=64)
    discharge_port = models.CharField(max_length=64)
    ship_arrival_date = models.DateField(blank=True, null=True)
    ship_departure_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.loading_port}-{self.discharge_port} ({self.ship_arrival_date}/{self.ship_departure_date})'


class Vehicle(models.Model):
    booking = models.ForeignKey(Booking, blank=True, null=True, on_delete=models.CASCADE)
    vin = models.CharField(unique=True, primary_key=True, max_length=17)
    make = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    weight = models.IntegerField('Weight(lbs)', blank=True, null=True)

    def __str__(self):
        return f'{self.make} {self.model} ({self.vin})'