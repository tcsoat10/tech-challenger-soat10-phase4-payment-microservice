
from config.database import DELETE_MODE
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class DeletePaymentStatusUseCase: 
    
    def __init__(self, payment_status_gateway: IPaymentStatusRepository):
        self.payment_status_gateway = payment_status_gateway
        
    @classmethod
    def build(cls, payment_status_gateway: IPaymentStatusRepository) -> 'DeletePaymentStatusUseCase':
        return cls(payment_status_gateway)
    
    def execute(self, payment_status_id: int) -> None:
        payment_status = self.payment_status_gateway.get_by_id(payment_status_id)
        if not payment_status:
            raise EntityNotFoundException(entity_name="PaymentStatus")
        
        if DELETE_MODE == 'soft':
            if payment_status.is_deleted():
                raise EntityNotFoundException(entity_name="PaymentStatus")

            payment_status.soft_delete()
            self.payment_status_gateway.update(payment_status)
        else:
            self.payment_status_gateway.delete(payment_status)
