"""
  Mildly customized serializers to enable dynamically altering data
   returned by serializers via query params.
"""

#pylint: disable=R0903
#pylint: disable=R0201

from rest_framework import serializers
from django.core.exceptions import SuspiciousOperation
from .models import Client, Event, Customer, Ticket


class DynamicModelSerializer(serializers.ModelSerializer):
    """
     Extension of the model serializer class to dynamically alter
      the fields of the serializer upon runtime.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the DynamicModelSerializer -- inherits the standard ModelSerializer
        Defined and automatically calls alter_fields so we aren't repeating ourselves
         on every serializer.
        :param args: Standard serializer args.  Just passed along.
        :param kwargs: Standard serializer kwargs.  Just passed along.
        """
        super(DynamicModelSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request'):
            self.alter_fields(self.context.get("request"), self.fields)


    def alter_fields(self, request, fields):
        """
        Dynamically alters the available fields on the object depending on the
         query params on the request.
        Operates through side effects rather than returns.
        :param request: Request object from django rest framework's context.
        :param fields: BindingDict containing the fields in the serializer to be altered
        :return: None, but has side effects
        """

        if request:
            exclude_fields = []
            if request.query_params.get('exclude_fields'):
                exclude_fields = request.query_params.get('exclude_fields').split(",")
            include_fields = []
            if request.query_params.get('embed_fields'):
                include_fields += request.query_params.get('embed_fields').split(",")
            if request.query_params.get('include_fields'):
                include_fields += request.query_params.get('include_fields').split(",")
            keys = fields.keys()
            if include_fields and exclude_fields:
                raise SuspiciousOperation(
                    'Cannot both include and exclude fields in the same API request.'
                )
            if include_fields:
                for field in set(keys):
                    if field not in include_fields:
                        fields.pop(field)
            if exclude_fields:
                for field in set(keys):
                    if field in exclude_fields:
                        fields.pop(field)


class ClientSerializer(DynamicModelSerializer):
    """
     Almost-standard serializer for the client endpoints.
    """

    class Meta:
        """
        Meta class for the client serializer
        """

        model = Client
        fields = ('__all__')


class EventSerializer(DynamicModelSerializer):
    """
     Almost-standard serializer for the event endpoints.
     Has a dynamic method for returning related objects and/or keys.
    """

    client = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the event serializer
        """

        model = Event
        fields = ('__all__')

    def get_client(self, obj):
        """
        Dynamically sets the 'client' field based on query params.
        :param obj: Object passed in by django rest framework by default.
        :return: Either a ClientSerializer or a UUID depending on query params.
        """

        request = self.context.get('request')
        if request:
            embed_fields = request.query_params.get('embed_fields')
            if embed_fields and 'client' in embed_fields:
                return ClientSerializer(instance=obj.client).data
        return obj.client_id


class CustomerSerializer(DynamicModelSerializer):
    """
     Almost-standard serializer for the customer endpoints.
    """

    class Meta:
        """
        Meta class for the customer serializer
        """

        model = Customer
        fields = ('__all__')

class TicketSerializer(DynamicModelSerializer):
    """
     Almost-standard serializer for the ticket endpoints.
     Has a dynamic method for returning related objects and/or keys.
    """

    customer = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the ticket serializer
        """

        model = Ticket
        fields = ('__all__')

    def get_customer(self, obj):
        """
        Dynamically sets the 'customer' field based on query params.
        :param obj: Object passed in by django rest framework by default.
        :return: Either a CustomerSerializer or a UUID depending on query params.
        """

        request = self.context.get('request')
        if request:
            embed_fields = request.query_params.get('embed_fields')
            if embed_fields and 'customer' in embed_fields:
                return CustomerSerializer(instance=obj.customer).data
        return obj.customer_id
    def get_event(self, obj):
        """
        Dynamically sets the 'event' field based on query params.
        :param obj: Object passed in by django rest framework by default.
        :return: Either a EventSerializer or a UUID depending on query params.
        """

        request = self.context.get('request')
        if request:
            embed_fields = request.query_params.get('embed_fields')
            if embed_fields and 'event' in embed_fields:
                return EventSerializer(instance=obj.event).data
        return obj.event_id
