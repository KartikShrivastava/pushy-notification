from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.serializers.send_bulk_notification_request import SendBulkNotificationRequestSerializer  # noqa: E501


class SendBulkNotificationsView(APIView):
    def post(self, request):
        request_serializer = SendBulkNotificationRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            return Response(request_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
