from datetime import datetime
from typing import Optional
from src.core.domain.entities.base_entity import BaseEntity


class PaymentMethod(BaseEntity):

    def __init__(
        self,
        name: str,
        description: str,
        payments: Optional[list] = [],
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._name = name
        self._description = description
        self._payments = payments

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def payments(self) -> list:
        return self._payments

    @payments.setter
    def payments(self, value: list) -> None:
        from src.core.domain.entities.payment import Payment
        if not all(isinstance(payment, Payment) for payment in value):
            raise ValueError("All items in payments must be instances of Payment")
        self._payments = value

__all__ = ["PaymentMethod"]
