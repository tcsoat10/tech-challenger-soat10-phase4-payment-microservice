from src.application.usecases.payment_usecase.payment_provider_webhook_handler_use_case import PaymentProviderWebhookHandlerUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.domain.dtos.payment.qr_code_payment_dto import QrCodePaymentDTO
from src.application.usecases.payment_usecase.process_payment_usecase import ProcessPaymentUseCase
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.core.ports.payment.i_payment_repository import IPaymentRepository


class PaymentController:
    
    def __init__(
        self,
        payment_provider_gateway: IPaymentProviderGateway, 
        payment_gateway: IPaymentRepository, 
        payment_status_gateway: IPaymentStatusRepository, 
        payment_method_gateway: IPaymentMethodRepository
    ):
        self.payment_provider_gateway: IPaymentProviderGateway = payment_provider_gateway
        self.payment_gateway: IPaymentRepository = payment_gateway
        self.payment_status_gateway: IPaymentStatusRepository = payment_status_gateway
        self.payment_method_gateway: IPaymentMethodRepository = payment_method_gateway
        
    def process_payment(self, method_payment: str) -> QrCodePaymentDTO:
        process_payment_use_case = ProcessPaymentUseCase.build(
            payment_gateway=self.payment_gateway,
            payment_status_gateway=self.payment_status_gateway,
            payment_method_gateway=self.payment_method_gateway,
            payment_provider_gateway=self.payment_provider_gateway,
        )
        payment = process_payment_use_case.execute(method_payment)
        return DTOPresenter.transform_from_dict(payment, QrCodePaymentDTO)

    def payment_provider_webhook(self, payload: dict) -> dict:
        payment_provider_webhook_use_case = PaymentProviderWebhookHandlerUseCase.build(
            self.payment_provider_gateway,
            self.payment_gateway,
            self.payment_status_gateway
        )
        return payment_provider_webhook_use_case.execute(payload)
            
