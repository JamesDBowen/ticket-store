from django import test
import unittest
from django.urls import reverse
from .views import Client, Event, Customer, Ticket
from .serializers import ClientSerializer, EventSerializer, CustomerSerializer, TicketSerializer
from rest_framework import status

client = test.Client()

class TestGetClient(test.TestCase):
    """ Test module for get client API """

    def setUp(self):
        self.clients = dict()
        self.clients["burning_man"] = Client.objects.create(
            name='Burning Man')
        self.clients["comic-con"] = Client.objects.create(
            name='Comic-Con')
        self.clients["pest-world"] = Client.objects.create(
            name='PestWorld')

    def test_get_client(self):
        response = client.get("/api/client/{}".format(str(self.clients["burning_man"].id)))
        client_object = Client.objects.get(id=self.clients["burning_man"].id)
        serializer = ClientSerializer(client_object)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_clients(self):
        response = client.get("/api/client")
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exclude_name(self):
        response = client.get("/api/client/{}?exclude_fields=name".format((self.clients["burning_man"].id)))
        self.assertTrue("name" not in response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestGetEvent(test.TestCase):
    """ Test module for get client API """

    def setUp(self):
        self.client = Client.objects.create(
            name='Burning Man')
        self.events = dict()
        self.events["burning_man_2018"] = Event.objects.create(
            name='Burning Man 2018', venue_capacity=1000, client_id=self.client.id)
        self.events["burning_man_2019"] = Event.objects.create(
            name='Burning Man 2018', venue_capacity=1000, client_id=self.client.id)

    def test_get_event(self):
        # get API response
        response = client.get("/api/event/{}".format(str(self.events["burning_man_2019"].id)))
        # get data from db
        event_object = Event.objects.get(id=self.events["burning_man_2019"].id)
        serializer = EventSerializer(event_object)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_events(self):
        response = client.get("/api/event")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_embed_client(self):
        # get API response
        response = client.get("/api/event/{}?embed_fields=client".format(str(self.events["burning_man_2018"].id)))
        # get data from db
        client_object = Client.objects.get(id=self.client.id)
        serializer = ClientSerializer(client_object)
        print("Response data:", response.data)
        print("Serializer data:", serializer.data)
        self.assertEqual(response.data["client"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestGetCustomer(test.TestCase):
    """ Test module for get client API """

    def setUp(self):
        self.customers = dict()
        self.customers["james_bowen"] = Customer.objects.create(
            name='James Bowen')
        self.customers["amanda-arias"] = Customer.objects.create(
            name='Amanda Arias')
        self.customers["beau-jeppesen"] = Customer.objects.create(
            name='Beau Jeppesen')

    def test_get_customer(self):
        # get API response
        response = client.get("/api/customer/{}".format(str(self.customers["james_bowen"].id)))
        # get data from db
        customer_object = Customer.objects.get(id=self.customers["james_bowen"].id)
        serializer = CustomerSerializer(customer_object)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_customers(self):
        response = client.get("/api/customer")
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_include_name(self):
        # get API response
        response = client.get("/api/customer/{}?include_fields=name".format(str(self.customers["james_bowen"].id)))
        # get data from db
        self.assertEqual(response.data["name"], "James Bowen")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestGetTicket(test.TestCase):
    """ Test module for get client API """

    def setUp(self):
        self.client = Client.objects.create(name='Burning Man')
        self.events = dict()
        self.events["burning_man_2018"] = Event.objects.create(
            name='Burning Man 2018',
            venue_capacity=1000,
            client_id=self.client.id
        )
        self.events["burning_man_2019"] = Event.objects.create(
            name='Burning Man 2018',
            venue_capacity=1000,
            client_id=self.client.id
        )
        self.customers = dict()
        self.customers["james_bowen"] = Customer.objects.create(name='James Bowen')
        self.customers["amanda_arias"] = Customer.objects.create(name='Amanda Arias')
        self.customers["beau_jeppesen"] = Customer.objects.create(name='Beau Jeppesen')
        self.tickets = dict()
        self.tickets["burning_man_2018_james_bowen"] = Ticket.objects.create(
            event_id=self.events["burning_man_2018"].id,
            customer_id=self.customers["james_bowen"].id,
            price=190.0
        )
        self.tickets["burning_man_2018_amanda_arias"] = Ticket.objects.create(
            event_id=self.events["burning_man_2018"].id,
            customer_id=self.customers["amanda_arias"].id,
            price=190.0
        )
        self.tickets["burning_man_2018_beau_jeppesen"] = Ticket.objects.create(
            event_id=self.events["burning_man_2018"].id,
            customer_id=self.customers["beau_jeppesen"].id,
            price=190.0
        )
        self.tickets["burning_man_2019_james_bowen"] = Ticket.objects.create(
            event_id=self.events["burning_man_2019"].id,
            customer_id=self.customers["james_bowen"].id,
            price=190.0
        )

    def test_get_ticket(self):
        # get API response
        response = client.get("/api/ticket/{}".format(str(self.tickets["burning_man_2018_james_bowen"].id)))
        # get data from db
        ticket_object = Ticket.objects.get(id=self.tickets["burning_man_2018_james_bowen"].id)
        serializer = TicketSerializer(ticket_object)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_tickets(self):
        response = client.get("/api/ticket")
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_embed_everything(self):
        # get API response
        response = client.get("/api/ticket/{}?embed_fields=event,customer".format(str(self.tickets["burning_man_2019_james_bowen"].id)))
        # get data from db
        event_object = Event.objects.get(id=self.events["burning_man_2019"].id)
        customer_object = Customer.objects.get(id=self.customers["james_bowen"].id)
        event_serializer = EventSerializer(event_object)
        customer_serializer = CustomerSerializer(customer_object)
        self.assertEqual(response.data["event"], event_serializer.data)
        self.assertEqual(response.data["customer"], customer_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)