
from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.entities.payment_method import PaymentMethod


class IPaymentMethodRepository(ABC):

    @abstractmethod
    def create(self, payment_method: PaymentMethod) -> PaymentMethod:
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> PaymentMethod:
        pass

    @abstractmethod
    def get_by_id(self, payment_method_id: str) -> PaymentMethod:
        pass

    @abstractmethod
    def get_all(self, include_deleted: Optional[bool] = False) -> list[PaymentMethod]:
        pass

    @abstractmethod
    def update(self, payment_method: PaymentMethod) -> PaymentMethod:
        pass

    @abstractmethod
    def delete(self, payment_method: PaymentMethod) -> None:
        pass
