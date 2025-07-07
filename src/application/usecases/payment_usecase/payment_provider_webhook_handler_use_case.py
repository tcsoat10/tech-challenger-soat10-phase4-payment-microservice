
import traceback
from src.constants.payment_status import PaymentStatusEnum
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class PaymentProviderWebhookHandlerUseCase:
    
    def __init__(
        self,
        payment_provider_gateway: IPaymentProviderGateway,
        payment_gateway: IPaymentRepository,
        payment_status_gateway: IPaymentStatusRepository,
    ):
        self.payment_provider_gateway = payment_provider_gateway
        self.payment_gateway = payment_gateway
        self.payment_status_gateway = payment_status_gateway
    
    @classmethod    
    def build(
        cls,
        payment_provider_gateway: IPaymentProviderGateway,
        payment_gateway: IPaymentRepository,
        payment_status_gateway: IPaymentStatusRepository
    ) -> 'PaymentProviderWebhookHandlerUseCase':
        return cls(
            payment_provider_gateway=payment_provider_gateway,
            payment_gateway=payment_gateway,
            payment_status_gateway=payment_status_gateway
        )
        
    def execute(self, payload: dict) -> None:
        """
        Processes a webhook sent by the payment service.
        :param payload: Data sent by the payment service webhook.
        """
        try:
            payment_details = self.payment_provider_gateway.verify_payment(payload)
            if payment_details.get("action") == "return":
                return payment_details

            external_reference = payment_details.get("external_reference")
            status_name = payment_details.get("payment_status")

            status_mapped = self.payment_provider_gateway.status_map(status_name)
            if not status_mapped:
                raise BadRequestException(f"Status desconhecido recebido: {status_name}")

            # Buscando o pagamento no banco de dados
            payment = self.payment_gateway.get_payment_by_reference(external_reference)
            if not payment:
                raise BadRequestException(f"Pagamento com referência {external_reference} não encontrado.")

            # Atualizando o status do pagamento
            new_status = self.payment_status_gateway.get_by_name(status_mapped.status)
            if not new_status:
                raise BadRequestException(f"Status de pagamento não encontrado: {status_name}")

            payment = self.payment_gateway.update_payment_status(payment, new_status.id)

            if not payment.order:
                payment.order = []
                order = self.order_gateway.get_by_payment_id(payment.id)
                if not order:
                    cancelled_status = self.payment_status_gateway.get_by_name(PaymentStatusEnum.PAYMENT_CANCELLED.status)
                    self.payment_gateway.update_payment_status(payment, cancelled_status.id)
                    return {"message": "Pagamento cancelado, pedido não encontrado."}
                
                payment.order.append(order)

            # if (
            #     new_status.name == PaymentStatusEnum.PAYMENT_COMPLETED.status and
            #     payment.order[0].order_status.status == OrderStatusEnum.ORDER_PLACED.status
            # ):
            #     payment.order[0].advance_order_status(self.order_status_gateway)
            #     self.order_gateway.update(payment.order[0])

        except Exception as e:
            traceback.print_exc()
            raise BadRequestException(f"Erro ao processar webhook: {str(e)}")
