import uuid

from django.db import models


class Payload(models.Model):
    payload_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.payload_id}'
