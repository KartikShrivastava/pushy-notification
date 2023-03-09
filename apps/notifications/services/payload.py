from django.forms import ValidationError

from apps.notifications.models.payload import Payload
from apps.notifications.serializers.payload import PayloadSerializer


class PayloadService:
    @classmethod
    def create_payload(cls, request_data):
        payload_serializer = PayloadSerializer(data=request_data)
        payload_serializer.is_valid(raise_exception=True)
        validated_data = payload_serializer.validated_data

        if request_data['title'] == '':
            raise ValidationError(message='Cannont insert payload with empty title')
        if request_data['body'] == '':
            raise ValidationError(message='Cannot insert payload with empty body')

        serialized_payload = PayloadSerializer(Payload.objects.create(
                                                **validated_data)).data
        return serialized_payload

    @classmethod
    def get_all_payloads(cls):
        payloads = Payload.objects.all()
        payload_serializers = PayloadSerializer(payloads, many=True)
        return payload_serializers.data
