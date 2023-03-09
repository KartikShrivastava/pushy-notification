from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.serializers.subscriber import SubscriberSerializer


class SubscriberService:
    @classmethod
    def create_subscriber(cls, request_data):
        subscriber_serializer = SubscriberSerializer(data=request_data)
        subscriber_serializer.is_valid(raise_exception=True)
        validated_data = subscriber_serializer.validated_data
        serialized_subscriber = SubscriberSerializer(Subscriber.objects.create(
                                                     **validated_data)).data
        return serialized_subscriber

    @classmethod
    def get_all_subscribers(cls):
        subscribers = Subscriber.objects.all()
        subscriber_serializers = SubscriberSerializer(subscribers, many=True)
        return subscriber_serializers.data
