from bson import ObjectId
import pytest
from unittest.mock import MagicMock

from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.domain.dtos.payment_method.update_payment_method_dto import UpdatePaymentMethodDTO
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.application.usecases.payment_method_usecase.create_payment_method_usecase import CreatePaymentMethodUseCase
from src.application.usecases.payment_method_usecase.delete_payment_method_usecase import DeletePaymentMethodUseCase
from src.application.usecases.payment_method_usecase.get_all_payment_methods_usecase import GetAllPaymentMethodsUseCase
from src.application.usecases.payment_method_usecase.get_payment_method_by_id_usecase import GetPaymentMethodByIdUseCase
from src.application.usecases.payment_method_usecase.get_payment_method_by_name_usecase import GetPaymentMethodByNameUseCase
from src.application.usecases.payment_method_usecase.update_payment_method_usecase import UpdatePaymentMethodUseCase


class TestPaymentMethodUseCases:

    @pytest.fixture
    def payment_method_gateway(self):
        return MagicMock()

    @pytest.fixture
    def payment_method(self):
        return PaymentMethod(name='credit_card', description='Credit Card', id=1)

    @pytest.fixture(autouse=True)
    def setup(self, payment_method_gateway):
        self.create_payment_method_usecase = CreatePaymentMethodUseCase(payment_method_gateway)
        self.delete_payment_method_usecase = DeletePaymentMethodUseCase(payment_method_gateway)
        self.get_all_payment_method_usecase = GetAllPaymentMethodsUseCase(payment_method_gateway)
        self.get_payment_method_by_id_usecase = GetPaymentMethodByIdUseCase(payment_method_gateway)
        self.get_payment_method_by_name_usecase = GetPaymentMethodByNameUseCase(payment_method_gateway)
        self.update_payment_method_usecase = UpdatePaymentMethodUseCase(payment_method_gateway)

    def test_create_payment_method_usecase(self, payment_method_gateway, payment_method):
        payment_method_gateway.get_by_name.return_value = None
        payment_method_gateway.create.return_value = payment_method

        dto = CreatePaymentMethodDTO(name='credit_card', description='Credit Card')
        result = self.create_payment_method_usecase.execute(dto)

        assert result.id == 1
        assert result.name == 'credit_card'
        assert result.description == 'Credit Card'
        payment_method_gateway.get_by_name.assert_called_once_with('credit_card')
        payment_method_gateway.create.assert_called_once()

    def test_create_payment_method_usecase_duplicated(self, payment_method_gateway, payment_method):
        payment_method_gateway.get_by_name.return_value = payment_method

        dto = CreatePaymentMethodDTO(name='credit_card', description='Credit Card')
        with pytest.raises(EntityDuplicatedException):
            self.create_payment_method_usecase.execute(dto)

    def test_create_payment_method_usecase_reactivate_deleted(self, payment_method_gateway, payment_method):
        deleted_method = PaymentMethod(name='credit_card', description='Original description', id=1)
        deleted_method.soft_delete()
        payment_method_gateway.get_by_name.return_value = deleted_method
        payment_method_gateway.update.return_value = payment_method

        dto = CreatePaymentMethodDTO(name='credit_card', description='Updated description')
        result = self.create_payment_method_usecase.execute(dto)

        assert result.id == 1
        assert result.name == 'credit_card'
        assert not result.is_deleted()
        payment_method_gateway.update.assert_called_once()

    def test_delete_payment_method_usecase_soft_delete(self, payment_method_gateway, payment_method, monkeypatch):
        monkeypatch.setattr("config.database.DELETE_MODE", "soft")
        payment_method_gateway.get_by_id.return_value = payment_method

        self.delete_payment_method_usecase.execute(1)

        assert payment_method.is_deleted()
        payment_method_gateway.update.assert_called_once_with(payment_method)

    def test_delete_payment_method_usecase_hard_delete(self, payment_method_gateway, payment_method, monkeypatch):
        monkeypatch.setattr("config.database.DELETE_MODE", "hard")
        payment_method_gateway.get_by_id.return_value = payment_method

        self.delete_payment_method_usecase.execute(1)

        payment_method_gateway.update.assert_called_once_with(payment_method)

    def test_delete_payment_method_not_found(self, payment_method_gateway):
        payment_method_gateway.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException):
            self.delete_payment_method_usecase.execute(999)

    def test_get_all_payment_method_usecase(self, payment_method_gateway, payment_method):
        payment_method_gateway.get_all.return_value = [payment_method]

        result = self.get_all_payment_method_usecase.execute()

        assert len(result) == 1
        assert result[0].name == 'credit_card'
        payment_method_gateway.get_all.assert_called_once()

    def test_get_payment_method_by_id_usecase(self, payment_method_gateway, payment_method):
        payment_method_gateway.get_by_id.return_value = payment_method

        result = self.get_payment_method_by_id_usecase.execute(1)

        assert result.id == 1
        assert result.name == 'credit_card'
        payment_method_gateway.get_by_id.assert_called_once_with(1)

    def test_get_payment_method_by_id_usecase_not_found(self, payment_method_gateway):
        payment_method_gateway.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException):
            self.get_payment_method_by_id_usecase.execute(999)

    def test_get_payment_method_by_name_usecase(self, payment_method_gateway, payment_method):
        payment_method_gateway.get_by_name.return_value = payment_method

        result = self.get_payment_method_by_name_usecase.execute('credit_card')

        assert result.id == 1
        assert result.name == 'credit_card'
        payment_method_gateway.get_by_name.assert_called_once_with('credit_card')

    def test_get_payment_method_by_name_usecase_not_found(self, payment_method_gateway):
        payment_method_gateway.get_by_name.return_value = None

        with pytest.raises(EntityNotFoundException):
            self.get_payment_method_by_name_usecase.execute('nonexistent')

    def test_update_payment_method_usecase(self, payment_method_gateway, payment_method):
        payment_method_gateway.get_by_id.return_value = payment_method
        payment_method_gateway.update.return_value = payment_method
        payment_method_gateway.exists_by_name.return_value = False
        
        fake_id = str(ObjectId())
        dto = UpdatePaymentMethodDTO(id=fake_id, name='debit_card', description='Debit Card')
        result = self.update_payment_method_usecase.execute(fake_id, dto)

        assert result.id == 1
        assert result.name == 'debit_card'
        assert result.description == 'Debit Card'
        payment_method_gateway.get_by_id.assert_called_once_with(fake_id)
        payment_method_gateway.update.assert_called_once_with(payment_method)

    def test_update_payment_method_usecase_not_found(self, payment_method_gateway):
        payment_method_gateway.get_by_id.return_value = None

        fake_id = str(ObjectId())
        dto = UpdatePaymentMethodDTO(id=fake_id, name='debit_card', description='Debit Card')
        with pytest.raises(EntityNotFoundException):
            self.update_payment_method_usecase.execute(fake_id, dto)