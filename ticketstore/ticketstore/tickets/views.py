"""
 Views for the tickets app
 Currently only consists of standard Django REST Framework viewsets
"""
#pylint: disable=E1101
#pylint: disable=R0901

from rest_framework import viewsets
from .models import Client, Event, Customer, Ticket
from .serializers import ClientSerializer, EventSerializer, CustomerSerializer, TicketSerializer

class ClientViewSet(viewsets.ModelViewSet):
    """
    Standard Django REST Framework viewset for Client objects.
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    Standard Django REST Framework viewset for Client objects.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    Standard Django REST Framework viewset for Client objects.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class TicketViewSet(viewsets.ModelViewSet):
    """
    Standard Django REST Framework viewset for Client objects.
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
