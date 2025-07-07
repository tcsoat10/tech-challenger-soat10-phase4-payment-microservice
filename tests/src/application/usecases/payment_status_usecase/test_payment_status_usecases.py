from bson import ObjectId
import pytest
from unittest.mock import MagicMock

from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.update_payment_status_dto import UpdatePaymentStatusDTO
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.application.usecases.payment_status_usecase.create_payment_status_usecase import CreatePaymentStatusUseCase
from src.application.usecases.payment_status_usecase.delete_payment_status_usecase import DeletePaymentStatusUseCase
from src.application.usecases.payment_status_usecase.get_all_payment_status_usecase import GetAllPaymentStatusUsecase
from src.application.usecases.payment_status_usecase.get_payment_status_by_id_usecase import GetPaymentStatusByIdUseCase
from src.application.usecases.payment_status_usecase.get_payment_status_by_name_usecase import GetPaymentStatusByNameUseCase
from src.application.usecases.payment_status_usecase.update_payment_status_usecase import UpdatePaymentStatusUseCase


class TestPaymentStatusUseCases:

    @pytest.fixture
    def payment_status_gateway(self):
        return MagicMock()

    @pytest.fixture
    def payment_status(self):
        fake_id = str(ObjectId())
        return PaymentStatus(name='pending', description='Payment pending', id=fake_id)

    @pytest.fixture(autouse=True)
    def setup(self, payment_status_gateway):
        self.create_payment_status_usecase = CreatePaymentStatusUseCase(payment_status_gateway)
        self.delete_payment_status_usecase = DeletePaymentStatusUseCase(payment_status_gateway)
        self.get_all_payment_status_usecase = GetAllPaymentStatusUsecase(payment_status_gateway)
        self.get_payment_status_by_id_usecase = GetPaymentStatusByIdUseCase(payment_status_gateway)
        self.get_payment_status_by_name_usecase = GetPaymentStatusByNameUseCase(payment_status_gateway)
        self.update_payment_status_usecase = UpdatePaymentStatusUseCase(payment_status_gateway)

    def test_create_payment_status_usecase(self, payment_status_gateway, payment_status):
        payment_status_gateway.get_by_name.return_value = None
        payment_status_gateway.create.return_value = payment_status

        dto = CreatePaymentStatusDTO(name='pending', description='Payment pending')
        result = self.create_payment_status_usecase.execute(dto)

        assert result.id == payment_status.id
        assert result.name == 'pending'
        assert result.description == 'Payment pending'
        payment_status_gateway.get_by_name.assert_called_once_with('pending')
        payment_status_gateway.create.assert_called_once()

    def test_create_payment_status_usecase_duplicated(self, payment_status_gateway, payment_status):
        payment_status_gateway.get_by_name.return_value = payment_status

        dto = CreatePaymentStatusDTO(name='pending', description='Payment pending')
        with pytest.raises(EntityDuplicatedException):
            self.create_payment_status_usecase.execute(dto)

    def test_create_payment_status_usecase_reactivate_deleted(self, payment_status_gateway, payment_status):
        deleted_status = PaymentStatus(name='pending', description='Original description', id=1)
        deleted_status.soft_delete()
        payment_status_gateway.get_by_name.return_value = deleted_status
        payment_status_gateway.update.return_value = payment_status

        dto = CreatePaymentStatusDTO(name='pending', description='Updated description')
        result = self.create_payment_status_usecase.execute(dto)

        assert result.id == 1
        assert result.name == 'pending'
        assert not result.is_deleted()
        payment_status_gateway.update.assert_called_once()

    def test_delete_payment_status_usecase_soft_delete(self, payment_status_gateway, payment_status, monkeypatch):
        monkeypatch.setattr("config.database.DELETE_MODE", "soft")
        payment_status_gateway.get_by_id.return_value = payment_status

        self.delete_payment_status_usecase.execute(1)

        assert payment_status.is_deleted()
        payment_status_gateway.update.assert_called_once_with(payment_status)

    def test_delete_payment_status_usecase_hard_delete(self, payment_status_gateway, payment_status, monkeypatch):
        monkeypatch.setattr("config.database.DELETE_MODE", "hard")
        payment_status_gateway.get_by_id.return_value = payment_status

        self.delete_payment_status_usecase.execute(1)

        payment_status_gateway.update.assert_called_once_with(payment_status)

    def test_delete_payment_status_not_found(self, payment_status_gateway):
        payment_status_gateway.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException):
            self.delete_payment_status_usecase.execute(999)

    def test_get_all_payment_status_usecase(self, payment_status_gateway, payment_status):
        payment_status_gateway.get_all.return_value = [payment_status]

        result = self.get_all_payment_status_usecase.execute()

        assert len(result) == 1
        assert result[0].name == 'pending'
        payment_status_gateway.get_all.assert_called_once()

    def test_get_payment_status_by_id_usecase(self, payment_status_gateway, payment_status):
        payment_status_gateway.get_by_id.return_value = payment_status

        result = self.get_payment_status_by_id_usecase.execute(1)

        assert result.id == payment_status.id
        assert result.name == 'pending'
        payment_status_gateway.get_by_id.assert_called_once_with(1)

    def test_get_payment_status_by_id_usecase_not_found(self, payment_status_gateway):
        payment_status_gateway.get_by_id.return_value = None

        with pytest.raises(EntityNotFoundException):
            self.get_payment_status_by_id_usecase.execute(999)

    def test_get_payment_status_by_name_usecase(self, payment_status_gateway, payment_status):
        payment_status_gateway.get_by_name.return_value = payment_status

        result = self.get_payment_status_by_name_usecase.execute(name='pending')

        assert result.id == payment_status.id
        assert result.name == 'pending'
        payment_status_gateway.get_by_name.assert_called_once_with(name='pending')

    def test_get_payment_status_by_name_usecase_not_found(self, payment_status_gateway):
        payment_status_gateway.get_by_name.return_value = None

        with pytest.raises(EntityNotFoundException):
            self.get_payment_status_by_name_usecase.execute('nonexistent')

    def test_update_payment_status_usecase(self, payment_status_gateway, payment_status):
        payment_status_gateway.get_by_id.return_value = payment_status
        payment_status_gateway.update.return_value = payment_status

        dto = UpdatePaymentStatusDTO(id=payment_status.id, name='completed', description='Payment completed')
        result = self.update_payment_status_usecase.execute(payment_status.id, dto)

        assert result.id == payment_status.id
        assert result.name == 'completed'
        assert result.description == 'Payment completed'
        payment_status_gateway.get_by_id.assert_called_once_with(payment_status.id)
        payment_status_gateway.update.assert_called_once_with(payment_status)

    def test_update_payment_status_usecase_not_found(self, payment_status_gateway):
        payment_status_gateway.get_by_id.return_value = None

        fake_id = str(ObjectId())
        dto = UpdatePaymentStatusDTO(id=fake_id, name='completed', description='Payment completed')
        with pytest.raises(EntityNotFoundException):
            self.update_payment_status_usecase.execute(fake_id, dto)
