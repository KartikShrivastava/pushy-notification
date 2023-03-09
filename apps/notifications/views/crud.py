from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.services.payload import PayloadService


class NotificationPayloadCRUDView(APIView):
    def get(self, request):
        payload_serializers = PayloadService.get_all_payloads()
        return Response(payload_serializers, status=status.HTTP_200_OK)

    def post(self, request):
        payload_serializer = PayloadService.create_payload(request_data=request.data)
        return Response(payload_serializer, status=status.HTTP_201_CREATED)
