
from pydantic import BaseModel, Field

from src.core.domain.entities.payment_status import PaymentStatus

class PaymentStatusDTO(BaseModel):
    id: str
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)

    @classmethod
    def from_entity(cls, payment_status: PaymentStatus):
        return cls(
            id=str(payment_status.id),
            name=payment_status.name,
            description=payment_status.description,
        )
