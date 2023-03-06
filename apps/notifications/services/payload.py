from apps.notifications.models.payload import Payload


class PayloadService:
    @classmethod
    def create_payload(cls, validated_data):
        inserted_payload = Payload.objects.create(**validated_data)
        return inserted_payload
