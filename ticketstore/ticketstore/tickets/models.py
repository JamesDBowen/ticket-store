from django.db import models
import uuid

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=512, null=False, blank=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=512, null=False, blank=False)
    venue_capacity = models.PositiveSmallIntegerField('Venue Capacity')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False, related_name='events')

    def __str__(self):
        return self.name


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=512, null=False, blank=False)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False, related_name='tickets')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=False, related_name='tickets')

    def __str__(self):
        return "{}: {}".format(self.event.name, self.customer.name)
