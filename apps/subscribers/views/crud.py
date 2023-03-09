from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.subscribers.services.subscriber import SubscriberService


class SubscriberCRUDView(APIView):
    def get(self, request):
        serialized_subscribers = SubscriberService.get_all_subscribers()
        return Response(serialized_subscribers, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_subscriber = SubscriberService.create_subscriber(
                                request_data=request.data)
        return Response(serialized_subscriber, status=status.HTTP_201_CREATED)
