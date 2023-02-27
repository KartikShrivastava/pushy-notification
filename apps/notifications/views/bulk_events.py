from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class SendBulkNotificationsView(APIView):
    # Request object expects list of subscriber_id and payload_id
    def post(self, request):
        print(request.data)
        return Response(status=status.HTTP_202_ACCEPTED)
