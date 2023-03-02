from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.serializers.send_bulk_notification_request import SendBulkNotificationRequestSerializer  # noqa: E501
from apps.notifications.services.notification import NotificationService


class SendBulkNotificationsView(APIView):
    def post(self, request):
        request_serializer = SendBulkNotificationRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        # TODO: fix error response is not being correctly generated with rabbitmq offline
        try:
            NotificationService().send_bulk_notifications(
                                subscriber_ids=request_serializer.data['subscriber_ids'],
                                payload_id=request_serializer.data['payload_id'])
            return Response({
                    'message': 'Web push notifications scheduled successfully'
            }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({
                'error': e
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
