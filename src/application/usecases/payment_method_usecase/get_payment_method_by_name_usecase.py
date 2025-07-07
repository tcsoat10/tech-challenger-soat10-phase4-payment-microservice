
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class GetPaymentMethodByNameUseCase:
    def __init__(self, payment_method_gateway: IPaymentMethodRepository):
        self.payment_method_gateway = payment_method_gateway
        
    @classmethod
    def build(cls, payment_method_gateway: IPaymentMethodRepository) -> 'GetPaymentMethodByNameUseCase':
        return cls(payment_method_gateway)
    
    def execute(self, name: str) -> PaymentMethod:
        payment_method = self.payment_method_gateway.get_by_name(name)
        if not payment_method:
            raise EntityNotFoundException(entity_name='Payment method')
        
        return payment_method

