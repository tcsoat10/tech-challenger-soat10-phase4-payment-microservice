
from src.core.domain.dtos.payment_method.update_payment_method_dto import UpdatePaymentMethodDTO
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class UpdatePaymentMethodUseCase:
    
    def __init__(self, payment_method_gateway: IPaymentMethodRepository):
        self.payment_method_gateway = payment_method_gateway
        
    @classmethod
    def build(cls, payment_method_gateway: IPaymentMethodRepository) -> 'UpdatePaymentMethodUseCase':
        return cls(payment_method_gateway)
    
    def execute(self, payment_method_id: str, dto: UpdatePaymentMethodDTO) -> PaymentMethod:
        payment_method = self.payment_method_gateway.get_by_id(payment_method_id)
        if not payment_method:
            raise EntityNotFoundException(entity_name='Payment method')

        if self.payment_method_gateway.exists_by_name(dto.name):
            raise EntityDuplicatedException(entity_name='Payment method')

        payment_method.name = dto.name
        payment_method.description = dto.description
        payment_method = self.payment_method_gateway.update(payment_method)
        
        return payment_method
