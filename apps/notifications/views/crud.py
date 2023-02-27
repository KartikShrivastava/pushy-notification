from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.serializers.payload import PayloadSerializer


class NotificationPayloadCRUDView(APIView):
    def post(self, request):
        payload_serializer = PayloadSerializer(data=request.data)
        if payload_serializer.is_valid():
            payload_serializer.save()
            return Response(payload_serializer.data, status=status.HTTP_201_CREATED)
        return Response(payload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
