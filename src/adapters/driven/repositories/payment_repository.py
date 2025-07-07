
from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel
from src.adapters.driven.repositories.models.payment_model import PaymentModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.payment import Payment
from src.core.ports.payment.i_payment_repository import IPaymentRepository


class PaymentRepository(IPaymentRepository):
    """
    Implementação concreta do repositório de pagamentos, responsável pela interação com o banco de dados.
    """

    def __init__(self):
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create_payment(self, payment: Payment) -> Payment:
        """
        Insere um novo pagamento na coleção `payments` e retorna o pagamento criado.
        :param payment: Instância do pagamento a ser criado.
        :return: Instância do pagamento criado.
        """
        if payment.id is not None:
            existing_payment = self.identity_map.get(Payment, payment.id)
            if existing_payment is not None:
                self.identity_map.remove(payment)

        payment_model = PaymentModel.from_entity(payment)
        payment_model.save()
        return payment_model.to_entity()
        

    def update_payment_status(self, payment: Payment, status_id) -> Payment:
        """
        Atualiza o status de um pagamento na coleção `payments`.
        :param payment: Instância do pagamento a ser atualizado.
        :param status_id: Novo ID do status do pagamento.
        :return: Instância do pagamento atualizado.
        """
        if payment.id is not None:
            existing_payment = self.identity_map.get(Payment, payment.id)
            if existing_payment is not None:
                self.identity_map.remove(payment)

        payment_status = PaymentStatusModel.objects(id=status_id).first()
        if payment_status is None:
            raise ValueError(f"Payment status with ID {status_id} does not exist.")

        # Find existing payment document
        payment_model = PaymentModel.objects(id=payment.id).first()
        if payment_model:
            
            payment_model.payment_status = payment_status
            payment_model.save()
        else:
            # Create new payment with updated status
            payment_model = PaymentModel.from_entity(payment)
            payment_model.payment_status = payment_status
            payment_model.save()

        return payment_model.to_entity()

    def get_payment_by_id(self, payment_id) -> Payment:
        """
        Recupera os detalhes de um pagamento pelo ID.
        :param payment_id: ID do pagamento.
        :return: Instância do pagamento.
        """
        payment_model = PaymentModel.objects(id=payment_id).first()
        if payment_model is None:
            return None

        return payment_model.to_entity()
        

    def get_payment_by_reference(self, external_reference: str) -> Payment:
        """
        Recupera os detalhes de um pagamento pela referência externa.
        :param external_reference: Referência externa do pagamento.
        :return: Instância do pagamento.
        """
        payment_model = PaymentModel.objects(external_reference=external_reference).first()
        if payment_model is None:
            return None
        return payment_model.to_entity()
        