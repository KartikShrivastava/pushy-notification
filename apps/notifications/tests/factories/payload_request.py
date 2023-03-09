import factory
from faker import Faker


class PayloadRequestFactory(factory.Factory):
    class Meta:
        model = dict

    @classmethod
    def create(cls, **kwargs):
        faker = Faker()
        Faker.seed(0)

        return {
            'title': faker.text(max_nb_chars=30),
            'body': faker.text(max_nb_chars=120),
        }
