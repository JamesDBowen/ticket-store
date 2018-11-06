"""
 Models for the ticket app -- nothing really special here.
"""

import uuid
from django.db import models

class Client(models.Model):
    """
    Model used to represent organizations putting on events.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=512, null=False, blank=False)

    def __str__(self):
        """ String representation of client, mostly for Django admin """
        return self.name


class Event(models.Model):
    """
    Model used to represent events.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=512, null=False, blank=False)
    venue_capacity = models.PositiveSmallIntegerField('Venue Capacity')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='events'
    )

    def __str__(self):
        """ String representation of event, mostly for Django admin """
        return self.name


class Customer(models.Model):
    """
    Model used to represent customers who have purchased event tickets.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=512, null=False, blank=False)

    def __str__(self):
        """ String representation of customer, mostly for Django admin """
        return self.name

class Ticket(models.Model):
    """
    Model used to represent event tickets.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='tickets'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='tickets'
    )

    def __str__(self):
        """ String representation of ticket, mostly for Django admin """
        return "{}: {}".format(self.event.name, self.customer.name)
