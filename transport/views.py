from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Booking, Vehicle
from transport.serializers import BookingSerializer, VehicleSerializer


class BookingViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        Booking.objects.create(**serializer.validated_data)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Booking.objects.all()
        booking = get_object_or_404(queryset, pk=pk)
        serializer = BookingSerializer(booking, context={'request': request})
        booking_vehicles = list(Vehicle.objects.filter(booking=booking).values("vin","make","model","weight"))
        response_data = serializer.data
        response_data['booking_vehicles'] = booking_vehicles
        return Response(response_data)
    
    def partial_update(self, request, pk=None):
        queryset = Booking.objects.all()
        booking = get_object_or_404(queryset, pk=pk)
        serializer = BookingSerializer(booking, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Booking.objects.all()
        booking = get_object_or_404(queryset, pk=pk)
        serializer = BookingSerializer(booking, context={'request': request})
        Booking.delete(booking)
        return Response(serializer.data)

    def list(self, request):
        queryset = Booking.objects.all().order_by('ship_arrival_date')
        serializer = BookingSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    permission_classes = [permissions.IsAuthenticated]


class VehicleViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = VehicleSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        Vehicle.objects.create(**serializer.validated_data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        serializer = VehicleSerializer(vehicle, context={'request': request})
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        queryset = Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        queryset = Vehicle.objects.all()
        vehicle = get_object_or_404(queryset, pk=pk)
        serializer = VehicleSerializer(vehicle, context={'request': request})
        Vehicle.delete(vehicle)
        return Response(serializer.data)

    def list(self, request):
        queryset = Vehicle.objects.all().order_by('booking')
        serializer = VehicleSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    permission_classes = [permissions.IsAuthenticated]
