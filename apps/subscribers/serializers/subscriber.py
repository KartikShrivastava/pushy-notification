from rest_framework import serializers

from apps.subscribers.models.subscriber import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

    def create(self, validated_data):
        inserted_subscriber = Subscriber.objects.create(**validated_data)
        return inserted_subscriber
