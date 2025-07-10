import traceback
import datetime
from src.core.ports.notification.i_notification_service import INotificationService
from src.constants.payment_status import PaymentStatusEnum
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
import logging

logger = logging.getLogger(__name__)

class PaymentProviderWebhookHandlerUseCase:
    
    def __init__(
        self,
        payment_provider_gateway: IPaymentProviderGateway,
        payment_gateway: IPaymentRepository,
        payment_status_gateway: IPaymentStatusRepository,
        notification_service: INotificationService,
    ):
        self.payment_provider_gateway = payment_provider_gateway
        self.payment_gateway = payment_gateway
        self.payment_status_gateway = payment_status_gateway
        self.notification_service = notification_service
    
    @classmethod    
    def build(
        cls,
        payment_provider_gateway: IPaymentProviderGateway,
        payment_gateway: IPaymentRepository,
        payment_status_gateway: IPaymentStatusRepository,
        notification_service: INotificationService = None
    ) -> 'PaymentProviderWebhookHandlerUseCase':
        return cls(
            payment_provider_gateway=payment_provider_gateway,
            payment_gateway=payment_gateway,
            payment_status_gateway=payment_status_gateway,
            notification_service=notification_service
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

            if (
                new_status.name == PaymentStatusEnum.PAYMENT_COMPLETED.status and 
                payment.notification_url and
                payment.client_notified is False and
                self.notification_service
            ):
                payment_data = {
                    'payment_id': str(payment.id),
                    'external_reference': payment.external_reference,
                    'amount': payment.amount,
                    'status': payment.payment_status.name,
                    'transaction_id': payment.transaction_id,
                    'timestamp': datetime.datetime.now(datetime.UTC).isoformat()
                }
                
                try:
                    self.notification_service.send_payment_notification(
                        payment.notification_url,
                        payment_data
                    )
                    logger.info(f"Notificação para pagamento {payment.id} enviada com sucesso.")
                    payment.mark_client_notified()
                    self.payment_gateway.update_payment(payment)
                except Exception as e:
                    logger.error(f"Falha ao enviar notificação para pagamento {payment.id} após todas as tentativas. Erro: {e}")
                    
        except Exception as e:
            traceback.print_exc()
            raise BadRequestException(f"Erro ao processar webhook: {str(e)}")
