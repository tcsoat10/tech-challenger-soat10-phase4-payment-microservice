
from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class CreatePaymentStatusUseCase:
    
    def __init__(self, payment_status_gateway: IPaymentStatusRepository):
        self.payment_status_gateway = payment_status_gateway
    
    @classmethod
    def build(cls, payment_status_gateway: IPaymentStatusRepository) -> 'CreatePaymentStatusUseCase':
        return cls(payment_status_gateway)
    
    def execute(self, dto: CreatePaymentStatusDTO) -> PaymentStatusDTO:
        payment_status = self.payment_status_gateway.get_by_name(dto.name)
        
        if payment_status:
            if not payment_status.is_deleted():
                raise EntityDuplicatedException(entity_name="PaymentStatus")
            
            payment_status.name = dto.name
            payment_status.description = dto.description
            payment_status.reactivate()
            self.payment_status_gateway.update(payment_status)
        else:
            payment_status = PaymentStatus(name=dto.name, description=dto.description)
            payment_status = self.payment_status_gateway.create(payment_status)

        return payment_status
    
