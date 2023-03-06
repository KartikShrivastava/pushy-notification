from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.serializers.subscriber import SubscriberSerializer
from apps.subscribers.services.subscriber import SubscriberService


class SubscriberCRUDView(APIView):
    def get(self, request):
        subscribers = Subscriber.objects.all()
        subscriber_serializer = SubscriberSerializer(subscribers, many=True)
        return Response(subscriber_serializer.data)

    def post(self, request):
        subscriber_serializer = SubscriberSerializer(data=request.data)
        subscriber_serializer.is_valid(raise_exception=True)
        SubscriberService.create_subscriber(
            validated_data=subscriber_serializer.validated_data)
        return Response(subscriber_serializer.data, status=status.HTTP_201_CREATED)
