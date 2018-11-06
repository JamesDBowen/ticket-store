"""
 Testing file for the serializers.  Has 5 test cases, each of which tests a a serializer/endpoint
  against the database and in-memory stored data
  OR tests the dynamic model serializer functionality.
"""

#pylint: disable=E1101
#pylint: disable=C0103

from django import test
from rest_framework import status
from .views import Client, Event, Customer, Ticket
from .serializers import ClientSerializer, EventSerializer, CustomerSerializer, TicketSerializer


client = test.Client()

class TestGetClient(test.TestCase):
    """
      Test module for client endpoints
    """

    def setUp(self):
        """
        Setting up test data for the client endpoints.
        :return: None
        """
        self.clients = dict()
        self.clients["burning_man"] = Client.objects.create(
            name='Burning Man')
        self.clients["comic-con"] = Client.objects.create(
            name='Comic-Con')
        self.clients["pest-world"] = Client.objects.create(
            name='PestWorld')

    def test_get_client(self):
        """
        Testing the get of a single client for having the correct status
         and returning the correct objects.
        :return: None
        """

        response = client.get("/api/client/{}".format(str(self.clients["burning_man"].id)))
        client_object = Client.objects.get(id=self.clients["burning_man"].id)
        serializer = ClientSerializer(client_object)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_clients(self):
        """
        Testing the get of all clients for having the correct status
         and returning the correct number of objects.
        :return: None
        """

        response = client.get("/api/client")
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestGetEvent(test.TestCase):
    """
      Test module for event endpoints
    """

    def setUp(self):
        """
        Setting up test data for the event endpoints.
        :return: None
        """
        self.client = Client.objects.create(
            name='Burning Man')
        self.events = dict()
        self.events["burning_man_2018"] = Event.objects.create(
            name='Burning Man 2018', venue_capacity=1000, client_id=self.client.id)
        self.events["burning_man_2019"] = Event.objects.create(
            name='Burning Man 2018', venue_capacity=1000, client_id=self.client.id)

    def test_get_event(self):
        """
        Testing the get of a single event for having the correct status
         and returning the correct objects.
        :return: None
        """

        # get API response
        response = client.get("/api/event/{}".format(str(self.events["burning_man_2019"].id)))
        # get data from db
        event_object = Event.objects.get(id=self.events["burning_man_2019"].id)
        serializer = EventSerializer(event_object)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_events(self):
        """
        Testing the get of all events for having the correct status
         and returning the correct number of objects.
        :return: None
        """

        response = client.get("/api/event")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestGetCustomer(test.TestCase):
    """
      Test module for customer endpoints
    """

    def setUp(self):
        """
        Setting up test data for the customer endpoints.
        :return: None
        """

        self.customers = dict()
        self.customers["james_bowen"] = Customer.objects.create(
            name='James Bowen')
        self.customers["amanda-arias"] = Customer.objects.create(
            name='Amanda Arias')
        self.customers["beau-jeppesen"] = Customer.objects.create(
            name='Beau Jeppesen')

    def test_get_customer(self):
        """
        Testing the get of a single customer for having the correct status
         and returning the correct objects.
        :return: None
        """

        # get API response
        response = client.get("/api/customer/{}".format(str(self.customers["james_bowen"].id)))
        # get data from db
        customer_object = Customer.objects.get(id=self.customers["james_bowen"].id)
        serializer = CustomerSerializer(customer_object)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_customers(self):
        """
        Testing the get of all customers for having the correct status
         and returning the correct number of objects.
        :return: None
        """

        response = client.get("/api/customer")
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestGetTicket(test.TestCase):
    """
      Test module for the ticket endpoints
    """

    def setUp(self):
        """
        Setting up test data for the ticket endpoints.
        :return: None
        """

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
        """
        Testing the get of a single ticket for having the correct status
         and returning the correct objects.
        :return: None
        """

        response = client.get("/api/ticket/{}".format(
            str(self.tickets["burning_man_2018_james_bowen"].id)
        ))
        ticket_object = Ticket.objects.get(id=self.tickets["burning_man_2018_james_bowen"].id)
        serializer = TicketSerializer(ticket_object)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_tickets(self):
        """
        Testing the get of all tickets for having the correct status
         and returning the correct number of objects.
        :return: None
        """

        response = client.get("/api/ticket")
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestDynamicSerializer(test.TestCase):
    """
      Test module for dynamic serialization functionality
    """

    def setUp(self):
        """
        Setting up test data for the dynamic serializers
        Uses the same data as TestGetTicket, since it's pretty extensive.
        :return: None
        """

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

    def test_exclude_name(self):
        """
        Tests the exclude field functionality of the DynamicModelSerializer
        :return: None
        """

        response = client.get("/api/client/{}?exclude_fields=name"
                              .format((self.client.id)))
        self.assertTrue("name" not in response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_embed_and_include(self):
        """
        Tests the embed and include include field functionality of the DynamicModelSerializer
        :return: None
        """

        response = client.get("/api/ticket/{}?embed_fields=event&include_fields=customer"
                              .format(str(self.tickets["burning_man_2019_james_bowen"].id)))
        event_object = Event.objects.get(id=self.events["burning_man_2019"].id)
        event_serializer = EventSerializer(event_object)
        self.assertEqual(response.data["event"], event_serializer.data)
        self.assertEqual(response.data["customer"], self.customers["james_bowen"].id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_include_name(self):
        """
        Tests the include field functionality of the DynamicModelSerializer
        :return: None
        """

        response = client.get("/api/customer/{}?include_fields=name"
                              .format(str(self.customers["james_bowen"].id)))
        self.assertEqual(response.data["name"], "James Bowen")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_include_and_exclude_error(self):
        """
        Tests the include field functionality of the DynamicModelSerializer
        :return: None
        """

        response = client.get("/api/customer/{}?include_fields=name&exclude_fields=id"
                              .format(str(self.customers["james_bowen"].id)))
        print("Respone data:, response.data")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
