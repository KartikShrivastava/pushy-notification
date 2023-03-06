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
        # modify the request.data according to Subscriber model fields
        request.data['endpoint_url'] = request.data.get('endpoint')
        request.data['expiration_time'] = request.data.get('expirationTime')
        request.data['p256dh_key'] = request.data.get('keys').get('p256dh')
        request.data['auth_key'] = request.data.get('keys').get('auth')

        subscriber_serializer = SubscriberSerializer(data=request.data)
        if subscriber_serializer.is_valid():
            SubscriberService.create_subscriber(
                validated_data=subscriber_serializer.validated_data)
            return Response(subscriber_serializer.data, status=status.HTTP_201_CREATED)
        return Response(subscriber_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
