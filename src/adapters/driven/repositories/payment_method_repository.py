from typing import Optional
from bson import ObjectId

from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class PaymentMethodRepository(IPaymentMethodRepository):

    def __init__(self):
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create(self, payment_method: PaymentMethod) -> PaymentMethod:
        if payment_method.id is not None:
            existing_entity = self.identity_map.get(PaymentMethod, payment_method.id)
            if existing_entity:
                self.identity_map.remove(existing_entity)
        
        payment_method_model = PaymentMethodModel.from_entity(payment_method)
        payment_method_model.save()
        return payment_method_model.to_entity()
    
    def exists_by_name(self, name: str) -> bool:
        return PaymentMethodModel.objects(name=name).first() is not None
    
    def get_by_name(self, name: str) -> PaymentMethod:
        payment_method_model = PaymentMethodModel.objects(name=name).first()
        if payment_method_model is None:
            return None
        return payment_method_model.to_entity()
    
    def get_by_id(self, payment_method_id: ObjectId) -> PaymentMethod:
        payment_method_model = PaymentMethodModel.objects(id=payment_method_id).first()
        if payment_method_model is None:
            return None
        return payment_method_model.to_entity()
    
    def get_all(self, include_deleted: Optional[bool] = False) -> list[PaymentMethod]:
        if include_deleted:
            query = PaymentMethodModel.objects()
        else:
            query = PaymentMethodModel.objects(inactivated_at=None)
        
        payment_method_models = query.all()
        return [payment_method_model.to_entity() for payment_method_model in payment_method_models]
    
    def update(self, payment_method) -> PaymentMethod:
        if payment_method.id is not None:
            existing_entity = self.identity_map.get(PaymentMethod, payment_method.id)
            if existing_entity:
                self.identity_map.remove(existing_entity)
        
        # Find existing document and update it
        payment_method_model = PaymentMethodModel.objects(id=payment_method.id).first()
        if payment_method_model:
            payment_method_model.name = payment_method.name
            payment_method_model.description = payment_method.description
            payment_method_model.updated_at = payment_method.updated_at
            payment_method_model.inactivated_at = payment_method.inactivated_at
            payment_method_model.save()
        else:
            payment_method_model = PaymentMethodModel.from_entity(payment_method)
            payment_method_model.save()
        
        return payment_method_model.to_entity()
    
    def delete(self, payment_method) -> None:
        payment_method_model = PaymentMethodModel.objects(id=payment_method.id).first()
        if payment_method_model:
            payment_method_model.delete()
            self.identity_map.remove(payment_method)
