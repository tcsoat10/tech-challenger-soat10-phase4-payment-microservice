from typing import List, Optional
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.payment_status_controller import PaymentStatusController
from src.core.domain.dtos.payment_status.update_payment_status_dto import UpdatePaymentStatusDTO
from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO
from src.core.containers import Container


router = APIRouter()


@router.post(
    "/payment-status",
    response_model=PaymentStatusDTO,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
@inject
def create_payment_status(
    dto: CreatePaymentStatusDTO,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
):
    return controller.create_payment_status(dto)

@router.get(
    "/payment-status/{payment_status_name}/name",
    response_model=PaymentStatusDTO,
    status_code=status.HTTP_200_OK
)
@inject
def get_payment_status_by_name(
    payment_status_name: str,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller])
):
    return controller.get_payment_status_by_name(name=payment_status_name)

@router.get(
    "/payment-status/{payment_status_id}/id",
    response_model=PaymentStatusDTO,
    status_code=status.HTTP_200_OK
)
@inject
def get_payment_status_by_id(
    payment_status_id: str,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
):
    return controller.get_payment_status_by_id(payment_status_id=payment_status_id)

@router.get(
        "/payment-status",
        response_model=List[PaymentStatusDTO],
)
@inject
def get_all_payment_status(
    include_deleted: Optional[bool] = False,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
):
    return controller.get_all_payment_status(include_deleted=include_deleted)

@router.put(
    "/payment-status/{payment_status_id}",
    response_model=PaymentStatusDTO,
    include_in_schema=False
)
@inject
def update_payment_status(
    payment_status_id: str,
    dto: UpdatePaymentStatusDTO,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller])
):
    return controller.update_payment_status(payment_status_id, dto)

@router.delete(
    "/payment-status/{payment_status_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False
)
@inject
def delete_payment_status(
    payment_status_id: str,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
):
    controller.delete_payment_status(payment_status_id=payment_status_id)
