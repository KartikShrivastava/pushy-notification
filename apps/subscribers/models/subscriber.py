import uuid

from django.db import models


class Subscriber(models.Model):
    # TODO: Add base model and inherit from that
    subscriber_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint_url = models.CharField(unique=True, max_length=500, blank=False, default=None)
    expiration_time = models.DateTimeField(null=True)
    p256dh_key = models.CharField(max_length=200, blank=False, default=None)
    auth_key = models.CharField(max_length=200, blank=False, default=None)

    def __str__(self):
        return f'{self.subscriber_id}'
