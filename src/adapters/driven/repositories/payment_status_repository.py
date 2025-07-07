from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository

class PaymentStatusRepository(IPaymentStatusRepository):

    def __init__(self):
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create(self, payment_status: PaymentStatus) -> PaymentStatus:
        if payment_status.id is not None:
            existing_entity = self.identity_map.get(PaymentStatus, payment_status)
            if existing_entity:
                self.identity_map.remove(existing_entity)
        
        payment_status_model = PaymentStatusModel.from_entity(payment_status)
        payment_status_model.save()
        return payment_status_model.to_entity()
    
    def exists_by_name(self, name):
        return PaymentStatusModel.objects(name=name).first() is not None
    
    def get_by_name(self, name):
        payment_status_model = PaymentStatusModel.objects(name=name).first()
        if not payment_status_model:
            return None
        return payment_status_model.to_entity()
    
    def get_by_id(self, payment_status_id):
        payment_status_model = PaymentStatusModel.objects(id=payment_status_id).first()
        if not payment_status_model:
            return None
        return payment_status_model.to_entity()
    
    def get_all(self, include_deleted: bool = False):
        if include_deleted:
            query = PaymentStatusModel.objects()
        else:
            query = PaymentStatusModel.objects(inactivated_at=None)
        
        payment_status_models = query.all()
        return [payment_status_model.to_entity() for payment_status_model in payment_status_models]
    
    def update(self, payment_status: PaymentStatus):
        if payment_status.id is not None:
            existing_entity = self.identity_map.get(PaymentStatus, payment_status)
            if existing_entity:
                self.identity_map.remove(existing_entity)

        # Find existing document and update it
        payment_status_model = PaymentStatusModel.objects(id=payment_status.id).first()
        if payment_status_model:
            payment_status_model.name = payment_status.name
            payment_status_model.description = payment_status.description
            payment_status_model.updated_at = payment_status.updated_at
            payment_status_model.inactivated_at = payment_status.inactivated_at
            payment_status_model.save()
        else:
            payment_status_model = PaymentStatusModel.from_entity(payment_status)
            payment_status_model.save()
        
        return payment_status_model.to_entity()
    
    def delete(self, payment_status: PaymentStatus):
        payment_status_model = PaymentStatusModel.objects(id=payment_status.id).first()
        if payment_status_model:
            payment_status_model.delete()
            self.identity_map.remove(payment_status)
