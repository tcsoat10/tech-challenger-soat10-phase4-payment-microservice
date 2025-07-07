
from config.database import DELETE_MODE
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class DeletePaymentMethodUseCase:
    
    def __init__(self, payment_method_gateway: IPaymentMethodRepository):
        self.payment_method_gateway = payment_method_gateway
        
    @classmethod
    def build(cls, payment_method_gateway: IPaymentMethodRepository) -> 'DeletePaymentMethodUseCase':
        return cls(payment_method_gateway)
    
    def execute(self, payment_method_id: int) -> None:
        payment_method = self.payment_method_gateway.get_by_id(payment_method_id)
        
        if not payment_method:
            raise EntityNotFoundException(entity_name='Payment method')
        
        if DELETE_MODE == 'soft':
            if payment_method.is_deleted():
                raise EntityNotFoundException(entity_name="Payment method")

            payment_method.soft_delete()
            self.payment_method_gateway.update(payment_method)
        else:
            self.payment_method_gateway.delete(payment_method)
