from rest_framework import serializers

from .models import Booking, Vehicle


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Booking
        fields = [
            'booking_number',
            'loading_port',
            'discharge_port',
            'ship_departure_date',
            'ship_arrival_date',
        ]


class VehicleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
            'booking',
            'vin',
            'make',
            'model',
            'weight',
        ]
