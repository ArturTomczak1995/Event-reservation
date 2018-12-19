from tickets import models as tickets_models
from rest_framework import serializers


class OrderedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = tickets_models.OrderedTicket
        fields = ["id", "location", "event_type", "seats_bought", "price", "date"]