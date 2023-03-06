from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.models.payload import Payload
from apps.notifications.serializers.payload import PayloadSerializer
from apps.notifications.services.payload import PayloadService


class NotificationPayloadCRUDView(APIView):
    def get(self, request):
        payloads = Payload.objects.all()
        payload_serializer = PayloadSerializer(payloads, many=True)
        return Response(payload_serializer.data)

    def post(self, request):
        payload_serializer = PayloadSerializer(data=request.data)
        payload_serializer.is_valid(raise_exception=True)
        PayloadService.create_payload(validated_data=payload_serializer.validated_data)
        return Response(payload_serializer.data, status=status.HTTP_201_CREATED)
