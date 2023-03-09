import random
import string

import factory
from faker import Faker


class SubscriberRequestFactory(factory.Factory):
    class Meta:
        model = dict

    @classmethod
    def create(cls, **kwargs):
        faker = Faker()
        Faker.seed(0)

        return {
            'endpoint_url': faker.url() + ''.join(random.choices(
                                            string.ascii_letters + string.digits, k=250)),
            'expiration_time': faker.date_time(),
            'p256dh_key': ''.join(random.choices(string.ascii_letters + string.digits,
                                                 k=100)),
            'auth_key': ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        }
