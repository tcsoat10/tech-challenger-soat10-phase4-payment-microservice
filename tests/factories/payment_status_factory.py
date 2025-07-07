import factory
from faker import Faker
from factory.mongoengine import MongoEngineFactory

from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel

fake = Faker()

class PaymentStatusFactory(MongoEngineFactory):

    class Meta:
        model = PaymentStatusModel

    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
