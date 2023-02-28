from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.serializers.send_notification_request import SendNotificationRequestSerializer  # noqa: E501


class SendBulkNotificationsView(APIView):
    # Request object expects list of subscribers and payload
    def post(self, request):
        print(request.data)
        request_serializer = SendNotificationRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            return Response(request_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
