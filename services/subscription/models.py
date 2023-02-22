import uuid

from django.db import models, DatabaseError


class SubscriberManager(models.Manager):
    def insert_subscriber(self, subscriber):
        queryset = self.get_queryset()
        try:
            return queryset.create(endpoint_url=subscriber.endpoint_url,
                                   expiration_time=subscriber.expiration_time,
                                   p256dh_key=subscriber.p256dh_key,
                                   auth_key=subscriber.auth_key)
        except DatabaseError as e:
            raise e


class Subscriber(models.Model):
    subscriber_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint_url = models.CharField(unique=True, max_length=300)
    expiration_time = models.DateTimeField(null=True)
    p256dh_key = models.CharField(max_length=200)
    auth_key = models.CharField(max_length=200)

    objects = SubscriberManager()

    def __str__(self):
        return f'{self.endpoint_url}'
