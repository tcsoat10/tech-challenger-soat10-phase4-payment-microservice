from src.core.domain.entities.payment_method import PaymentMethod
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.constants.payment_status import PaymentStatusEnum
from src.core.domain.entities.base_entity import BaseEntity
from typing import Dict, Any, Optional


class Payment(BaseEntity):
    
    def __init__(
        self, 
        amount: float,
        external_reference: str,
        qr_code: Optional[str] = None,
        transaction_id: Optional[str] = None,
        payment_method: PaymentMethod = None, 
        payment_status: PaymentStatus = None,
        order: list = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        inactivated_at: Optional[str] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._payment_method = payment_method
        self._payment_status = payment_status
        self._amount = amount
        self._external_reference = external_reference
        self._qr_code = qr_code
        self._transaction_id = transaction_id
        self._order = order
    
    @property
    def payment_method(self):
        return self._payment_method

    @payment_method.setter
    def payment_method(self, value):
        self._payment_method = value

    @property
    def payment_status(self):
        return self._payment_status

    @payment_status.setter
    def payment_status(self, value):
        self._payment_status = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        self._amount = value

    @property
    def external_reference(self):
        return self._external_reference

    @external_reference.setter
    def external_reference(self, value):
        self._external_reference = value   

    @property
    def qr_code(self):
        return self._qr_code

    @qr_code.setter
    def qr_code(self, value):
        value = value.strip()
        if not value:
            raise ValueError("QR code cannot be empty")
        self._qr_code = value
        
    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value

    @property
    def transaction_id(self):
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Transaction ID cannot be empty")
        self._transaction_id = value
    
    def is_pending(self) -> bool:
        return self._payment_status.name == PaymentStatusEnum.PAYMENT_PENDING.status

    def is_completed(self) -> bool:
        return self._payment_status.name == PaymentStatusEnum.PAYMENT_COMPLETED.status
    
    def is_cancelled(self) -> bool:
        return self._payment_status.name == PaymentStatusEnum.PAYMENT_CANCELLED.status

    def update_status(self, new_payment_status: PaymentStatus):
        self.payment_status = new_payment_status

    def initiate_payment(self, payment_data: Dict[str, Any], payment_provider_gateway: IPaymentProviderGateway):
        payment_provider_response = payment_provider_gateway.initiate_payment(payment_data)
        self.qr_code = payment_provider_response.get("qr_data")
        self.transaction_id = payment_provider_response.get("in_store_order_id")
        return payment_provider_response


__all__ = ['Payment']
