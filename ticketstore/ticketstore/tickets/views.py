from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from .models import Client, Event, Customer, Ticket
from .serializers import ClientSerializer, EventSerializer, CustomerSerializer, TicketSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer