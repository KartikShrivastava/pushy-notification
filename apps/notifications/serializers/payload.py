from rest_framework import serializers

from apps.notifications.models.payload import Payload


class PayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payload
        fields = '__all__'

    def create(self, validated_data):
        inserted_payload = Payload.objects.create(**validated_data)
        return inserted_payload
