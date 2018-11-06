from django.contrib import admin
from ticketstore.tickets.models import Client, Event, Customer, Ticket
# Register your models here.

admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Customer)
admin.site.register(Ticket)
