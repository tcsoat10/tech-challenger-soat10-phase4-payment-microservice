
from mongoengine import StringField
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.payment_status import PaymentStatus
from src.adapters.driven.repositories.models.base_model import BaseModel


class PaymentStatusModel(BaseModel):
    meta = {'collection': 'payment_status'}

    name = StringField(max_length=50, required=True, unique=True)
    description = StringField(max_length=255, required=False)

    # Note: We'll handle the reverse reference to payments in the PaymentModel

    @classmethod
    def from_entity(cls, payment_status: PaymentStatus):
        return cls(
            name=payment_status.name,
            description=payment_status.description,
            id=payment_status.id,
            created_at=payment_status.created_at,
            updated_at=payment_status.updated_at,
            inactivated_at=payment_status.inactivated_at
        )
        
    def to_entity(self) -> PaymentStatus:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_entity = identity_map.get(PaymentStatus, self.id)
        if existing_entity:
            return existing_entity
        
        payment_status = PaymentStatus(
            name=self.name,
            description=self.description
        )
        identity_map.add(payment_status)
        
        # Load related payments if needed
        from src.adapters.driven.repositories.models.payment_model import PaymentModel
        payments = PaymentModel.objects(payment_status=self.id)
        payment_status.payments = [payment.to_entity() for payment in payments]
        
        payment_status.id = self.id
        payment_status.created_at = self.created_at
        payment_status.updated_at = self.updated_at
        payment_status.inactivated_at = self.inactivated_at
        
        return payment_status
        

__all__ = ["PaymentStatusModel"]
