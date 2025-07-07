
from typing import Any, Dict
from pydantic import BaseModel

class QrCodePaymentDTO(BaseModel):
    payment_id: int
    transaction_id: str
    qr_code_link: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QrCodePaymentDTO':
        return cls(
            payment_id=data["payment_id"],
            transaction_id=data["transaction_id"],
            qr_code_link=data["qr_code_link"]
        )
