from faker import Faker
from factory.mongoengine import MongoEngineFactory
import factory

from src.adapters.driven.repositories.models.payment_model import PaymentModel
from tests.factories.payment_method_factory import PaymentMethodFactory
from tests.factories.payment_status_factory import PaymentStatusFactory


fake = Faker()


class PaymentFactory(MongoEngineFactory):
    class Meta:
        model = PaymentModel    

    payment_method = factory.SubFactory(PaymentMethodFactory)
    payment_status = factory.SubFactory(PaymentStatusFactory)
    amount = factory.Faker('pyfloat', positive=True, min_value=1, max_value=1000)
    external_reference = factory.Faker('uuid4')
    qr_code = factory.LazyAttribute(lambda _: fake.url())
    transaction_id = factory.Faker('uuid4')
