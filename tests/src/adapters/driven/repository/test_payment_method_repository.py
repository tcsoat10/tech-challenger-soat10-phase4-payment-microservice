
import pytest

from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.core.domain.entities.payment_method import PaymentMethod
from tests.factories.payment_method_factory import PaymentMethodFactory
from mongoengine.errors import NotUniqueError


class TestPaymentMethodRepository:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = PaymentMethodRepository()
        self.clean_database()

    def clean_database(self):
        PaymentMethodModel.drop_collection()

    def test_create_payment_method_success(self):
        payment_method = PaymentMethod(name="Credit Card", description="Pay with credit card")
        created_payment_method = self.repository.create(payment_method)

        assert created_payment_method.id is not None
        assert created_payment_method.name == "Credit Card"
        assert created_payment_method.description == "Pay with credit card"

        db_payment_method = PaymentMethodModel.objects(name="Credit Card").first()
        assert db_payment_method is not None
        assert db_payment_method.name == "Credit Card"
        assert db_payment_method.description == "Pay with credit card"

    def test_try_create_payment_method_duplicated_with_repository_and_raise_error(self):
        PaymentMethodFactory(name="Credit Card", description="Pay with credit card")
        
        new = PaymentMethod(name="Credit Card", description="Pay with credit card")
        
        with pytest.raises(NotUniqueError):
            self.repository.create(new)
    
    def test_get_payment_method_by_name_success(self):
        PaymentMethodFactory(name="Credit Card", description="Pay with credit card")

        payment_method_from_db = self.repository.get_by_name("Credit Card")
        
        assert payment_method_from_db is not None
        assert payment_method_from_db.name == "Credit Card"
        assert payment_method_from_db.description == "Pay with credit card"

    def test_get_all_payment_methods_success(self):
        PaymentMethodFactory(name="Credit Card", description="Pay with credit card")
        PaymentMethodFactory(name="Debit Card", description="Pay with debit card")

        payment_methods_from_db = self.repository.get_all()
        
        assert len(payment_methods_from_db) == 2
        assert payment_methods_from_db[0].name == "Credit Card"
        assert payment_methods_from_db[0].description == "Pay with credit card"
        assert payment_methods_from_db[1].name == "Debit Card"
        assert payment_methods_from_db[1].description == "Pay with debit card"

    def test_get_all_payment_methods_empty(self):
        payment_methods_from_db = self.repository.get_all()
        
        assert len(payment_methods_from_db) == 0

    def test_update_payment_method_success(self):
        payment_method = PaymentMethodFactory(name="Credit Card", description="Pay with credit card")

        payment_method.name = "Debit Card"
        payment_method.description = "Pay with debit card"
        updated_payment_method = self.repository.update(payment_method)

        assert updated_payment_method.id is not None
        assert updated_payment_method.name == "Debit Card"
        assert updated_payment_method.description == "Pay with debit card"

        db_payment_method = PaymentMethodModel.objects(name="Debit Card").first()
        assert db_payment_method is not None
        assert db_payment_method.name == "Debit Card"
        assert db_payment_method.description == "Pay with debit card"

    def test_delete_payment_method_success(self):
        payment_method = PaymentMethodFactory(name="Credit Card", description="Pay with credit card")

        self.repository.delete(payment_method)

        db_payment_method = PaymentMethodModel.objects(name="Credit Card").first()
        assert db_payment_method is None
