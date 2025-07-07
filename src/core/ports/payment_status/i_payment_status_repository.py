from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.payment_status import PaymentStatus

class IPaymentStatusRepository(ABC):
    
    @abstractmethod
    def create(payment_status: PaymentStatus) -> PaymentStatus:
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> PaymentStatus:
        pass

    @abstractmethod
    def get_by_id(self, payment_status_id: str) -> PaymentStatus:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[PaymentStatus]:
        pass
    
    @abstractmethod
    def update(self, payment_status: PaymentStatus) -> PaymentStatus:
        pass

    @abstractmethod
    def delete(self, payment_status: PaymentStatus) -> None:
        pass
