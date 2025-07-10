
from typing import Any, Dict
from pydantic import BaseModel

from src.core.domain.entities.payment import Payment

class QrCodePaymentDTO(BaseModel):
    payment_id: str
    transaction_id: str
    qr_code_link: str
    
    # optional
    external_reference: str = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QrCodePaymentDTO':
        return cls(
            payment_id=data["payment_id"],
            transaction_id=data["transaction_id"],
            qr_code_link=data["qr_code_link"]
        )
        
    @classmethod
    def from_entity(cls, entity: Payment) -> 'QrCodePaymentDTO':
        return cls(
            payment_id=str(entity.id),
            transaction_id=entity.transaction_id,
            qr_code_link=entity.qr_code,
            external_reference=entity.external_reference or ""
        )
