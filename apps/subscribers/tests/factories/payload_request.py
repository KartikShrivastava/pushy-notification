import factory
from faker import Faker

faker = Faker()


class PayloadRequestFactory(factory.Factory):
    class Meta:
        model = dict

    title = faker.sentence(max_nb_chars=30)
    body = faker.text(max_nb_chars=30)
