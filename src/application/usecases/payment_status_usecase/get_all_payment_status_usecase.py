
from typing import List, Optional
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class GetAllPaymentStatusUsecase:

    def __init__(self, payment_status_gateway: IPaymentStatusRepository):
        self.payment_status_gateway = payment_status_gateway
        
    @classmethod
    def build(cls, payment_status_gateway: IPaymentStatusRepository) -> 'GetAllPaymentStatusUsecase':
        return cls(payment_status_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[PaymentStatus]:
        payment_status = self.payment_status_gateway.get_all(include_deleted=include_deleted)
        return payment_status
