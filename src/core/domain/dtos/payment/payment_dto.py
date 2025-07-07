from pydantic import BaseModel

from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO
from src.core.domain.entities.payment import Payment


class PaymentDTO(BaseModel):
    id: int
    payment_method: PaymentMethodDTO
    payment_status: PaymentStatusDTO

    @classmethod
    def from_entity(cls, payment: Payment) -> 'PaymentDTO':
        return cls(
            id=payment.id,
            payment_method=PaymentMethodDTO.from_entity(payment.payment_method),
            payment_status=PaymentStatusDTO.from_entity(payment.payment_status)
        )
