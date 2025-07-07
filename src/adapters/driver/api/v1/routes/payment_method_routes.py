from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.payment_method_controller import PaymentMethodController
from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO
from src.core.domain.dtos.payment_method.update_payment_method_dto import UpdatePaymentMethodDTO
from src.core.containers import Container


router = APIRouter()


@router.post(
    "/payment-methods",
    response_model=PaymentMethodDTO,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
@inject
def create_payment_method(
    dto: CreatePaymentMethodDTO,
    controller: PaymentMethodController = Depends(Provide[Container.payment_method_controller]),
):
    return controller.create_payment_method(dto)

@router.get(
    "/payment-methods/{payment_method_name}/name",
    response_model=PaymentMethodDTO,
    status_code=status.HTTP_200_OK
)
@inject
def get_payment_method_by_name(
    payment_method_name: str,
    controller: PaymentMethodController = Depends(Provide[Container.payment_method_controller]),
    # user: dict = Security(get_current_user)
):
    return controller.get_payment_method_by_name(name=payment_method_name)

@router.get(
    "/payment-methods/{payment_method_id}/id",
    response_model=PaymentMethodDTO,
    status_code=status.HTTP_200_OK,
)
@inject
def get_payment_method_by_id(
    payment_method_id: str,
    controller: PaymentMethodController = Depends(Provide[Container.payment_method_controller]),\
):
    return controller.get_payment_method_by_id(payment_method_id)

@router.get(
    "/payment-methods",
    response_model=list[PaymentMethodDTO],
    status_code=status.HTTP_200_OK,
)
@inject
def get_all_payment_methods(
    include_deleted: bool = False,
    controller: PaymentMethodController = Depends(Provide[Container.payment_method_controller]),
):
    return controller.get_all_payment_methods(include_deleted=include_deleted)

@router.put(
    "/payment-methods/{payment_method_id}",
    response_model=PaymentMethodDTO,
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
@inject
def update_payment_method(
    payment_method_id: str,
    dto: UpdatePaymentMethodDTO,
    controller: PaymentMethodController = Depends(Provide[Container.payment_method_controller]),
):
    return controller.update_payment_method(payment_method_id, dto)

@router.delete(
    "/payment-methods/{payment_method_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False
)
@inject
def delete_payment_method(
    payment_method_id: str,
    controller: PaymentMethodController = Depends(Provide[Container.payment_method_controller]),
):
    return controller.delete_payment_method(payment_method_id)
