
from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class CreatePaymentMethodUseCase:
    
    def __init__(self, payment_method_gateway: IPaymentMethodRepository):
        self.payment_method_gateway = payment_method_gateway
        
    @classmethod
    def build(cls, payment_method_gateway: IPaymentMethodRepository) -> 'CreatePaymentMethodUseCase':
        return cls(payment_method_gateway)
    
    def execute(self, dto: CreatePaymentMethodDTO):
        payment_method = self.payment_method_gateway.get_by_name(dto.name)
        if payment_method:
            if not payment_method.is_deleted():
                raise EntityDuplicatedException("Payment method")

            payment_method.name = dto.name
            payment_method.description = dto.description
            payment_method.reactivate()
            self.payment_method_gateway.update(payment_method)
        else:
            payment_method = PaymentMethod(name=dto.name, description=dto.description)
            payment_method = self.payment_method_gateway.create(payment_method)

        return payment_method
