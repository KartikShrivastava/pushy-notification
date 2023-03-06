from apps.subscribers.models.subscriber import Subscriber


class SubscriberService:
    @classmethod
    def create_subscriber(cls, validated_data):
        inserted_subscriber = Subscriber.objects.create(**validated_data)
        return inserted_subscriber
