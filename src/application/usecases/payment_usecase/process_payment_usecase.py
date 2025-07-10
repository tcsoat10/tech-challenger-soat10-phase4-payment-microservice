from typing import Any, Dict

from config.settings import WEBHOOK_URL
from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.constants.payment_status import PaymentStatusEnum
from src.core.domain.entities.payment import Payment
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
import uuid


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

    def execute(self, dto: CreatePaymentDTO) -> Payment:
        payment_method = self.payment_method_gateway.get_by_name(dto.payment_method)
        if not payment_method:
            raise EntityNotFoundException("Não foi possível encontrar o método de pagamento informado.")

        payment_status = self.payment_status_gateway.get_by_name(PaymentStatusEnum.PAYMENT_PENDING.status)
        if not payment_status:
            raise ValueError(f"Status de pagamento não encontrado: {PaymentStatusEnum.PAYMENT_PENDING.status}")

        payment = Payment(
            payment_method=payment_method,
            payment_status=payment_status,
            amount=dto.total_amount,
            external_reference=f"order-{str(uuid.uuid4())}",
            notification_url=dto.notification_url,
        )

        payment_data = {
            "title": dto.title,
            "description": dto.description,
            "total_amount": dto.total_amount,
            "external_reference": payment.external_reference,
            "payment_notification_url": f"{WEBHOOK_URL}/api/v1/webhook/payment",
            "items": [
                {
                    "title": item.name,
                    "description": item.description,
                    "category": item.category,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "unit_measure": "unit",
                    "total_amount": item.unit_price * item.quantity,
                }
                for item in dto.items
            ],
        }
        payment.initiate_payment(payment_data, self.payment_provider_gateway)
        payment = self.payment_gateway.create_payment(payment)

        return payment

