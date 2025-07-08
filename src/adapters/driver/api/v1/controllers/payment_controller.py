from src.application.usecases.payment_usecase.get_payment_by_id_usecase import GetPaymentByIdUseCase
from src.application.usecases.payment_usecase.get_payment_by_transaction_id_usecase import GetPaymentByTransactionIdUseCase
from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
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
        
    def process_payment(self, dto: CreatePaymentDTO) -> QrCodePaymentDTO:
        process_payment_use_case = ProcessPaymentUseCase.build(
            payment_gateway=self.payment_gateway,
            payment_status_gateway=self.payment_status_gateway,
            payment_method_gateway=self.payment_method_gateway,
            payment_provider_gateway=self.payment_provider_gateway,
        )
        payment = process_payment_use_case.execute(dto)
        return DTOPresenter.transform(payment, QrCodePaymentDTO)

    def get_payment_by_transaction_id(self, transaction_id: str) -> QrCodePaymentDTO:
        get_payment_by_transaction_id_use_case = GetPaymentByTransactionIdUseCase.build(self.payment_gateway)
        payment = get_payment_by_transaction_id_use_case.execute(transaction_id)
        if not payment:
            raise EntityNotFoundException(message="Pagamento não encontrado para o transaction_id informado.")
        return DTOPresenter.transform(payment, QrCodePaymentDTO)
    
    def get_payment_by_id(self, payment_id: str) -> QrCodePaymentDTO:
        get_payment_by_id_use_case = GetPaymentByIdUseCase.build(
            self.payment_gateway
        )
        payment = get_payment_by_id_use_case.execute(payment_id)
        if not payment:
            raise EntityNotFoundException("Pagamento não encontrado para o ID informado.")
        return DTOPresenter.transform(payment, QrCodePaymentDTO)

    def payment_provider_webhook(self, payload: dict) -> dict:
        payment_provider_webhook_use_case = PaymentProviderWebhookHandlerUseCase.build(
            self.payment_provider_gateway,
            self.payment_gateway,
            self.payment_status_gateway
        )
        return payment_provider_webhook_use_case.execute(payload)
            
