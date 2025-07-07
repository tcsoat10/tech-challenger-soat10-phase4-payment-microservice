
from typing import List, Optional
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class GetAllPaymentMethodsUseCase:
    def __init__(self, payment_method_gateway: IPaymentMethodRepository):
        self.payment_method_gateway = payment_method_gateway
        
    @classmethod
    def build(cls, payment_method_gateway: IPaymentMethodRepository) -> 'GetAllPaymentMethodsUseCase':
        return cls(payment_method_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[PaymentMethod]:
        payment_methods = self.payment_method_gateway.get_all(include_deleted=include_deleted)
        return payment_methods
    
        
