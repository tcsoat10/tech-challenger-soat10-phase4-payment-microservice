from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.core.domain.dtos.payment.qr_code_payment_dto import QrCodePaymentDTO
from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
from src.core.containers import Container

router = APIRouter()

# Criar pagamento para o pedido
@router.post(
    "/payment",
    response_model=QrCodePaymentDTO,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_payment(
    dto: CreatePaymentDTO,
    controller: PaymentController = Depends(Provide[Container.payment_controller]),
):
    return controller.process_payment(dto)

@router.get(
    "/payment/transaction/{transaction_id}",
    response_model=QrCodePaymentDTO,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_payment_by_transaction_id(
    transaction_id: str,
    controller: PaymentController = Depends(Provide[Container.payment_controller]),
):
    return controller.get_payment_by_transaction_id(transaction_id)

@router.get(
    "/payment/id/{payment_id}",
    response_model=QrCodePaymentDTO,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_payment_by_id(
    payment_id: str,
    controller: PaymentController = Depends(Provide[Container.payment_controller]),
):
    return controller.get_payment_by_id(payment_id)
