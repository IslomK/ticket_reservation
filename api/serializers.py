from rest_framework import serializers


class ReservationSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(required=True)
    client_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)


class PaymentSerializer(serializers.Serializer):
    total_cost = serializers.IntegerField(required=True)
    currency = serializers.CharField(required=True)