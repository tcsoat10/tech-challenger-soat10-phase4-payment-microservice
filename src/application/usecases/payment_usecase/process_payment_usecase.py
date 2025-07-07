from typing import Any, Dict

from config.settings import WEBHOOK_URL
from src.constants.payment_status import PaymentStatusEnum
from src.core.domain.entities.payment import Payment
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class ProcessPaymentUseCase:
    
    def __init__(self,
        payment_gateway: IPaymentRepository,
        payment_status_gateway: IPaymentStatusRepository,
        payment_method_gateway: IPaymentMethodRepository,
        payment_provider_gateway: IPaymentProviderGateway
    ):
        self.payment_gateway = payment_gateway
        self.payment_status_gateway = payment_status_gateway
        self.payment_method_gateway = payment_method_gateway
        self.payment_provider_gateway = payment_provider_gateway
        
    @classmethod
    def build(
        cls,
        payment_gateway: IPaymentRepository,
        payment_status_gateway: IPaymentStatusRepository,
        payment_method_gateway: IPaymentMethodRepository,
        payment_provider_gateway: IPaymentProviderGateway
    ) -> 'ProcessPaymentUseCase':
        return cls(
            payment_gateway=payment_gateway,
            payment_status_gateway=payment_status_gateway,
            payment_method_gateway=payment_method_gateway,
            payment_provider_gateway=payment_provider_gateway
        )

    def execute(self, method_payment: str) -> Dict[str, Any]:

        payment_method = self.payment_method_gateway.get_by_name(method_payment)
        if not payment_method:
            raise EntityNotFoundException("Não foi possível encontrar o método de pagamento informado.")

        # payment_data = order.prepare_payment_data(WEBHOOK_URL)

        # payment_status = self.payment_status_gateway.get_by_name(PaymentStatusEnum.PAYMENT_PENDING.status)
        # if not payment_status:
        #     raise ValueError(f"Status de pagamento não encontrado: {PaymentStatusEnum.PAYMENT_PENDING.status}")

        # payment = Payment(
        #     payment_method=payment_method,
        #     payment_status=payment_status,
        #     amount=payment_data['total_amount'],
        #     external_reference=payment_data["external_reference"],
        # )
        # payment_provider_response = payment.initiate_payment(payment_data, self.payment_provider_gateway)
        
        # payment = self.payment_gateway.create_payment(payment)
        # order.payment = payment
        # self.order_gateway.update(order)

        # return {
        #     "payment_id": payment.id,
        #     "transaction_id": payment_provider_response["in_store_order_id"],
        #     "qr_code_link": payment_provider_response["qr_data"]
        # }
        
        return {}
