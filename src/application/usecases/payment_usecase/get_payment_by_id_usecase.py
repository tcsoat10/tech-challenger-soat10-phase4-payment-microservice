from src.core.domain.entities.payment import Payment
from src.core.ports.payment.i_payment_repository import IPaymentRepository


class GetPaymentByIdUseCase:
    """Use case for retrieving a payment by ID."""
    
    def __init__(self, payment_gateway: IPaymentRepository):
        self.payment_gateway = payment_gateway
    
    @classmethod
    def build(cls, payment_gateway: IPaymentRepository) -> 'GetPaymentByIdUseCase':
        """Factory method to create an instance of GetPaymentByIdUseCase."""
        return cls(payment_gateway=payment_gateway)
    
    def execute(self, payment_id: str) -> Payment | None:
        """Execute the use case to retrieve a payment by ID."""
        payment = self.payment_gateway.get_payment_by_id(payment_id)
        return payment