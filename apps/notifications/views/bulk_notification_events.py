from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.serializers.send_bulk_notification_request import SendBulkNotificationRequestSerializer  # noqa: E501
from apps.notifications.services.notification import NotificationService


class SendBulkNotificationsView(APIView):
    def post(self, request):
        request_serializer = SendBulkNotificationRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            NotificationService().send_bulk_notifications(
                                  subscriber_ids=request_serializer.data['subscriber_ids'],
                                  payload_id=request_serializer.data['payload_id'])
            return Response(request_serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
