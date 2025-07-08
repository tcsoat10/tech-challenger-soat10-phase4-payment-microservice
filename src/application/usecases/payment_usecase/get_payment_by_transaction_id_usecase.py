from src.core.domain.entities.payment import Payment
from src.core.ports.payment.i_payment_repository import IPaymentRepository


class GetPaymentByTransactionIdUseCase:
    """Use case for retrieving a payment by its transaction ID."""
    
    def __init__(self, payment_gateway: IPaymentRepository):
        self.payment_gateway = payment_gateway
    
    @classmethod
    def build(cls, payment_gateway: IPaymentRepository) -> 'GetPaymentByTransactionIdUseCase':
        """Factory method to create an instance of GetPaymentByTransactionIdUseCase."""
        return cls(payment_gateway=payment_gateway)
    
    def execute(self, transaction_id: str) -> Payment | None:
        """Execute the use case to retrieve a payment by its transaction ID."""
        payment = self.payment_gateway.get_payment_by_transaction_id(transaction_id)
        return payment