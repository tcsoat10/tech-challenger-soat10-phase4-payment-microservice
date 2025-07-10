from mongoengine import StringField, FloatField, ReferenceField, BooleanField
from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.payment import Payment
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.base_entity import BaseEntity

from bson import ObjectId


class PaymentModel(BaseModel):
    meta = {'collection': 'payments'}

    payment_method = ReferenceField('PaymentMethodModel', required=False)
    payment_status = ReferenceField('PaymentStatusModel', required=True)

    amount = FloatField(default=0.0, required=True)
    external_reference = StringField(max_length=500, required=True)

    qr_code = StringField(max_length=500, required=False)
    transaction_id = StringField(max_length=100, required=False)
    
    notification_url = StringField(required=False)
    client_notified = BooleanField(default=False)

    @classmethod
    def from_entity(cls, payment: BaseEntity):
        payment_method_id = payment.payment_method.id if payment.payment_method else None
        payment_status_id = payment.payment_status.id if payment.payment_status else None
        
        if payment_method_id is None or ObjectId.is_valid(payment_method_id) is False:
            raise ValueError("Payment method is required")
        
        if payment_status_id is None or ObjectId.is_valid(payment_status_id) is False:
            raise ValueError("Payment status is required")

        return cls(
            payment_method = ObjectId(payment_method_id),
            payment_status = ObjectId(payment_status_id),
            amount=payment.amount,
            external_reference=payment.external_reference,
            qr_code=payment.qr_code,
            transaction_id=payment.transaction_id,
            notification_url=payment.notification_url,
            client_notified=payment.client_notified,
            id=payment.id,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
            inactivated_at=payment.inactivated_at
        )
    
    def to_entity(self) -> Payment:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_payment = identity_map.get(Payment, self.id)
        if existing_payment:
            return existing_payment

        payment = Payment(
            id=self.id,
            amount=self.amount,
            external_reference=self.external_reference,
            qr_code=self.qr_code,
            transaction_id=self.transaction_id,
            notification_url=self.notification_url,
            created_at=self.created_at,  
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
        )
        identity_map.add(payment)

        payment.payment_method = self._get_payment_method(identity_map)
        payment.payment_status = self._get_payment_status(identity_map)

        return payment
    
    def _get_payment_status(self, identity_map: IdentityMap):
        from src.core.domain.entities.payment_status import PaymentStatus
        from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel
        
        payment_status = identity_map.get(PaymentStatus, self.payment_status.id)
        if payment_status:
            return payment_status
        
        payment_status_model = PaymentStatusModel.objects(id=self.payment_status.id).first()
        if payment_status_model:
            return payment_status_model.to_entity()
        
        return None
    
    def _get_payment_method(self, identity_map: IdentityMap):
        from src.core.domain.entities.payment_method import PaymentMethod
        from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel

        payment_method = identity_map.get(PaymentMethod, self.payment_method.id)
        if payment_method:
            return payment_method

        payment_method_model = PaymentMethodModel.objects(id=self.payment_method.id).first()
        if payment_method_model:
            return payment_method_model.to_entity()
        
        return None
    

__all__ = ['PaymentModel']
