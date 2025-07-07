
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class GetPaymentStatusByNameUseCase:
    def __init__(self, payment_status_gateway: IPaymentStatusRepository):
        self.payment_status_gateway = payment_status_gateway
        
    @classmethod
    def build(cls, payment_status_gateway: IPaymentStatusRepository) -> 'GetPaymentStatusByNameUseCase':
        return cls(payment_status_gateway)
    
    def execute(self, name: str) -> PaymentStatus:
        payment_status = self.payment_status_gateway.get_by_name(name=name)
        if not payment_status:
            raise EntityNotFoundException(entity_name="PaymentStatus")
        
        return payment_status
