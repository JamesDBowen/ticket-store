from rest_framework import serializers
from .models import Client, Event, Customer, Ticket
from collections import OrderedDict
from django.db import models

class DynamicModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DynamicModelSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request'):
            self.alter_fields(self.context.get("request"), self.fields, self.Meta)


    def alter_fields(self, request, fields, meta):
        exclude_fields = []
        if request:
            if request.query_params.get('exclude_fields'):
                exclude_fields = request.query_params.get('exclude_fields').split(",")
            include_fields = []
            if request.query_params.get('embed_fields'):
                include_fields += request.query_params.get('embed_fields').split(",")
            if request.query_params.get('include_fields'):
                include_fields += request.query_params.get('include_fields').split(",")
            keys = fields.keys()
            if include_fields:
                for field in set(keys):
                    if field not in include_fields:
                        fields.pop(field)
            if exclude_fields:
                for field in set(keys):
                    if field in exclude_fields:
                        fields.pop(field)


class ClientSerializer(DynamicModelSerializer):
    class Meta:
        model = Client
        fields = ('__all__')
        abstract = True


class EventSerializer(DynamicModelSerializer):
    client = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('__all__')
        abstract = True

    def get_client(self, obj):
        request = self.context.get('request')
        if request:
            embed_fields = request.query_params.get('embed_fields')
            if embed_fields and 'client' in embed_fields:
                return ClientSerializer(instance=obj.client).data
        return obj.client_id


class CustomerSerializer(DynamicModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')
        abstract = True

class TicketSerializer(DynamicModelSerializer):
    customer = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ('__all__')
        abstract = True

    def get_customer(self, obj):
        request = self.context.get('request')
        if request:
            embed_fields = request.query_params.get('embed_fields')
            if embed_fields and 'customer' in embed_fields:
                return CustomerSerializer(instance=obj.customer).data
        return obj.customer_id
    def get_event(self, obj):
        request = self.context.get('request')
        if request:
            embed_fields = request.query_params.get('embed_fields')
            if embed_fields and 'event' in embed_fields:
                return EventSerializer(instance=obj.event).data
        return obj.event_id