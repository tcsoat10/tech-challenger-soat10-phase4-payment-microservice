import pytest

from mongoengine.errors import ValidationError

from src.core.exceptions.bad_request_exception import BadRequestException
from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel
from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel
from src.adapters.driven.repositories.models.payment_model import PaymentModel
from src.constants.payment_status import PaymentStatusEnum
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.adapters.driven.repositories.payment_repository import PaymentRepository
from src.core.domain.entities.payment import Payment
from tests.factories.payment_factory import PaymentFactory
from tests.factories.payment_method_factory import PaymentMethodFactory
from tests.factories.payment_status_factory import PaymentStatusFactory

class TestPaymentRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.payment_gateway: IPaymentRepository = PaymentRepository()
        self.clean_database()

    def clean_database(self):
        try:
            PaymentModel.drop_collection()
            PaymentMethodModel.drop_collection()
            PaymentStatusModel.drop_collection()
        except Exception:
            pass


    def test_create_payment_success(self):
        payment_method = PaymentMethodFactory()
        payment_status = PaymentStatusFactory()

        payment = Payment(
            payment_method=payment_method.to_entity(),
            payment_status=payment_status.to_entity(),
            amount=100.0,
            external_reference="123456",
            qr_code="QrCode",
            transaction_id="1234"
        )

        created_payment = self.payment_gateway.create_payment(payment)

        assert created_payment.id is not None
        assert created_payment.payment_method.id == payment_method.id
        assert created_payment.payment_status.id == payment_status.id
    
    def test_create_payment_invalid_data_raises_error(self):
        payment_method = PaymentMethodFactory()
        payment_status = PaymentStatusFactory()
        payment = Payment(
            payment_method=payment_method.to_entity(),
            payment_status=payment_status.to_entity(),
            amount=100.0,
            external_reference=None,  # Inválido
            qr_code="QrCode",
            transaction_id="1234"
        )

        with pytest.raises(ValidationError):
            self.payment_gateway.create_payment(payment)

    def test_get_payment_by_id_returns_none_unregistered_id(self):
        from bson import ObjectId
        fake_id = ObjectId()
        
        data = self.payment_gateway.get_payment_by_id(fake_id)

        assert data is None
        
    def test_payment_status_methods(self):
        pending_status = PaymentStatusFactory(name=PaymentStatusEnum.PAYMENT_PENDING.status)
        completed_status = PaymentStatusFactory(name=PaymentStatusEnum.PAYMENT_COMPLETED.status)
        cancelled_status = PaymentStatusFactory(name=PaymentStatusEnum.PAYMENT_CANCELLED.status)
        
        payment_pending_model = PaymentFactory(payment_status=pending_status)
        payment_completed_model = PaymentFactory(payment_status=completed_status)
        payment_cancelled_model = PaymentFactory(payment_status=cancelled_status)

        try:
            payment_pending = self.payment_gateway.get_payment_by_id(payment_pending_model.id)
        except Exception as ex:
            print(f"Error: {ex}")

        payment_completed = self.payment_gateway.get_payment_by_id(payment_completed_model.id)
        payment_cancelled = self.payment_gateway.get_payment_by_id(payment_cancelled_model.id)
        
        assert payment_pending.is_pending() is True
        assert payment_completed.is_completed() is True
        assert payment_cancelled.is_cancelled() is True
    
    def test_update_payments_payment_status_success(self):
        payment = PaymentFactory()
        payment_status = PaymentStatusFactory()

        updated_payment = self.payment_gateway.update_payment_status(payment, payment_status.id)

        assert updated_payment.id == payment.id
        assert updated_payment.payment_status.id == payment_status.id
        
    def test_update_payment_status_same_status(self):
        payment_status = PaymentStatusFactory()
        payment = PaymentFactory(payment_status=payment_status.id)
        
        # Atualiza com o mesmo status
        updated_payment = self.payment_gateway.update_payment_status(payment, payment_status.id)
        
        assert updated_payment.payment_status.id == payment_status.id
    
    def test_update_payments_payment_status_unregistered_id(self):
        payment = PaymentFactory()
        
        # Create a new ObjectId for testing
        from bson import ObjectId
        fake_status_id = ObjectId()

        with pytest.raises(ValueError) as exc_info:
            self.payment_gateway.update_payment_status(payment, fake_status_id)
            
        assert str(exc_info.value) == f"Payment status with ID {fake_status_id} does not exist."
        
    def test_get_payment_by_reference_success(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_reference(payment.external_reference)

        assert data is not None
        assert data.id == payment.id
        assert data.external_reference == payment.external_reference
        
    def test_get_payment_by_reference_returns_none_unregistered_reference(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_reference(payment.external_reference + "1")

        assert data is None
        
    def test_get_payment_by_transaction_id_success(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_transaction_id(payment.transaction_id)

        assert data is not None
        assert data.id == payment.id
        assert data.transaction_id == payment.transaction_id
    
    def test_get_payment_by_transaction_id_returns_none_unregistered_transaction_id(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_transaction_id(payment.transaction_id + "1")

        assert data is None
    
    def test_get_payment_by_id_success(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_id(payment.id)

        assert data is not None
        assert data.id == payment.id
        assert data.external_reference == payment.external_reference
        assert data.transaction_id == payment.transaction_id
        assert data.qr_code == payment.qr_code
        assert data.amount == payment.amount
        assert data.payment_method.id == payment.payment_method.id
        assert data.payment_status.id == payment.payment_status.id

    def test_get_payment_by_id_invalid_id(self):
        with pytest.raises(BadRequestException) as exc_info:
            self.payment_gateway.get_payment_by_id(123)

        assert str(exc_info.value) == "ID de pagamento inválido: 123"
