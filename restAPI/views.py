from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.subscription.serializers import SubscriberSerializer


class SubscriberView(APIView):
    def post(self, request):
        # modify the request.data according to Subscriber model fields
        request.data['endpoint_url'] = request.data.get('endpoint')
        request.data['expiration_time'] = request.data.get('expirationTime')
        request.data['p256dh_key'] = request.data.get('keys').get('p256dh')
        request.data['auth_key'] = request.data.get('keys').get('auth')

        subscriber_serializer = SubscriberSerializer(data=request.data)
        if subscriber_serializer.is_valid():
            subscriber_serializer.save()
            return Response(subscriber_serializer.data, status=status.HTTP_201_CREATED)
        return Response(subscriber_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
