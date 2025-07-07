
from src.core.domain.dtos.payment_status.update_payment_status_dto import UpdatePaymentStatusDTO
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class UpdatePaymentStatusUseCase: 
    
    def __init__(self, payment_status_gateway: IPaymentStatusRepository):
        self.payment_status_gateway = payment_status_gateway
        
    @classmethod
    def build(cls, payment_status_gateway: IPaymentStatusRepository) -> 'UpdatePaymentStatusUseCase':
        return cls(payment_status_gateway)
    
    def execute(self, payment_status_id: int, dto: UpdatePaymentStatusDTO) -> PaymentStatus:
        payment_status = self.payment_status_gateway.get_by_id(payment_status_id)
        if not payment_status:
            raise EntityNotFoundException(entity_name="PaymentStatus")
        
        payment_status.name = dto.name
        payment_status.description = dto.description
        updated_payment_status = self.payment_status_gateway.update(payment_status)
        
        return updated_payment_status
