from django.contrib.auth.models import User   
from rest_framework.test import APIRequestFactory, APITestCase

from .views import BookingViewSet, VehicleViewSet
from .models import Booking

from datetime import datetime, timedelta


class BookingsTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', email='testuser@testmail.com', password='testpassword')
        self.url = '/api/bookings/'
        self.booking_number = 'b466bd53-7737-4ede-802f-782f5c1331a8'
    
    def test_bookings_crud(self):

        # create
        view = BookingViewSet.as_view({'post':'create'})
        payload = {
            "booking_number": self.booking_number,
            "loading_port": "Port A",
            "discharge_port": "Port B",
            "ship_departure_date": datetime.date(datetime.now()),
            "ship_arrival_date": datetime.date(datetime.now()) + timedelta(days=7)
        }
        request = self.factory.post(self.url, data=payload, format='json')
        request.user = self.user
        response = view(request)
        assert response.status_code == 200
        assert response.data['loading_port'] == "Port A"


        booking_number = response.data['booking_number']
    
        # read
        view = BookingViewSet.as_view({'get':'retrieve'})
        request = self.factory.get(self.url)
        request.user = self.user
        response = view(request, pk=self.booking_number)
        assert response.status_code == 200
        assert response.data['loading_port'] == "Port A"

        # update
        view = BookingViewSet.as_view({'patch':'partial_update'})
        payload = {
            "loading_port": "Port C"
        }
        request = self.factory.patch(self.url, data=payload, format='json')
        request.user = self.user
        response = view(request, pk=self.booking_number)
        assert response.status_code == 200
        assert response.data['booking_number'] == self.booking_number
        assert response.data['loading_port'] == "Port C"

        # delete
        view = BookingViewSet.as_view({'delete':'destroy'})
        request = self.factory.delete(self.url)
        request.user = self.user
        response = view(request, pk=self.booking_number)
        assert response.status_code == 200
        
        # list
        view = BookingViewSet.as_view({'get': 'list'})
        request = self.factory.get(self.url)
        request.user = self.user
        response = view(request)
        assert response.status_code == 200
        assert response.data == []


class VehiclesTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', email='testuser@testmail.com', password='testpassword')
        self.url = '/api/vehicles/'
        self.vin = "0XXXX00X00X000000"
    
    def test_vehicles_crud(self):

        # create
        view = VehicleViewSet.as_view({'post':'create'})
        payload = {
            "booking": None,
            "vin": self.vin,
            "make": "Tester",
            "model": "Test",
            "weight": 9999
        }
        request = self.factory.post(self.url, data=payload, format='json')
        request.user = self.user
        response = view(request)
        assert response.status_code == 200
        assert response.data['vin'] == self.vin
    
        # read
        view = VehicleViewSet.as_view({'get':'retrieve'})
        request = self.factory.get(self.url)
        request.user = self.user
        response = view(request, pk=self.vin)
        assert response.status_code == 200
        assert response.data['vin'] == self.vin

        # update
        view = VehicleViewSet.as_view({'patch':'partial_update'})
        payload = {
            "make": "Another Tester"
        }
        request = self.factory.patch(self.url, data=payload, format='json')
        request.user = self.user
        response = view(request, pk=self.vin)
        assert response.status_code == 200
        assert response.data['vin'] == self.vin
        assert response.data['make'] == "Another Tester"

        # delete
        view = VehicleViewSet.as_view({'delete':'destroy'})
        request = self.factory.delete(self.url)
        request.user = self.user
        response = view(request, pk=self.vin)
        assert response.status_code == 200
        
        # list
        view = VehicleViewSet.as_view({'get': 'list'})
        request = self.factory.get(self.url)
        request.user = self.user
        response = view(request)
        assert response.status_code == 200
        assert response.data == []
   
