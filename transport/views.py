from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

import pyexcel as pe

from .models import Booking, Vehicle
from transport.serializers import BookingSerializer, VehicleSerializer


class BookingViewSet(viewsets.ViewSet):

    @extend_schema(
        request=[
          BookingSerializer
        ],
    )

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
        queryset = Booking.objects.all().order_by('ship_departure_date')
        serializer = BookingSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def export_xls(self, request):
        queryset = Booking.objects.all().order_by('ship_departure_date')
        serializer = BookingSerializer(queryset, many=True, context={'request': request})

        merged_sheet = pe.Sheet()
        i = 0
        for el in serializer.data:
            if i == 0:
                merged_sheet.row += pe.get_book(adict=el)['pyexcel_sheet1']
            else:
                merged_sheet.row += pe.get_book(adict=el)['pyexcel_sheet1'][1]
            i += 1

        merged_sheet.save_as("files/temp/bookings_list.xls")
        
        with open("files/temp/bookings_list.xls", 'rb') as f:
            data = f.read()

        response = HttpResponse(data, headers= {
            'Content-Type': 'application/vnd.ms-excel',
            'Content-Disposition': 'attachment; filename="bookings_list.xls"',
        })

        return response

    permission_classes = [permissions.IsAuthenticated]


class VehicleViewSet(viewsets.ViewSet):

    @extend_schema(
        request=[
          VehicleSerializer
        ],
    )

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
    
    @action(detail=False, methods=['get'])
    def export_xls(self, request):
        queryset = Vehicle.objects.all().order_by('booking')
        serializer = VehicleSerializer(queryset, many=True, context={'request': request})

        merged_sheet = pe.Sheet()
        i = 0
        for el in serializer.data:
            if i == 0:
                merged_sheet.row += pe.get_book(adict=el)['pyexcel_sheet1']
            else:
                merged_sheet.row += pe.get_book(adict=el)['pyexcel_sheet1'][1]
            i += 1

        merged_sheet.save_as("files/temp/vehicles_list.xls")
        
        with open("files/temp/vehicles_list.xls", 'rb') as f:
            data = f.read()

        response = HttpResponse(data, headers= {
            'Content-Type': 'application/vnd.ms-excel',
            'Content-Disposition': 'attachment; filename="vehicles_list.xls"',
        })

        return response



    permission_classes = [permissions.IsAuthenticated]
