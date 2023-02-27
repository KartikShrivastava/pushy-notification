from django.test import TestCase
from django.utils import timezone

from services.subscription.models import Subscriber


class SubscriberManagerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subscriber = Subscriber(endpoint_url='https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                                    expiration_time=timezone.now(),
                                    p256dh_key='BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                                    auth_key='vDfqsQPFWabqpmeFFv6EEg')
