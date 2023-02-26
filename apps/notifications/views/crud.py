from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.models.payload import Payload
from apps.notifications.serializers.payload import PayloadSerializer


class NotificationPayloadCRUDView(APIView):
    def get(self, request):
        payloads = Payload.objects.all()
        payload_serializer = PayloadSerializer(payloads, many=True)
        return Response(payload_serializer.data)

    def post(self, request):
        payload_serializer = PayloadSerializer(data=request.data)
        if payload_serializer.is_valid():
            payload_serializer.save()
            return Response(payload_serializer.data, status=status.HTTP_201_CREATED)
        return Response(payload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
