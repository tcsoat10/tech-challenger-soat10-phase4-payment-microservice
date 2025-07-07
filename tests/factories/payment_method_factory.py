import factory
from factory.mongoengine import MongoEngineFactory
from faker import Faker

from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel

fake = Faker()

class PaymentMethodFactory(MongoEngineFactory):

    class Meta:
        model = PaymentMethodModel

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
