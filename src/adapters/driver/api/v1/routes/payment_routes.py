from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
from src.core.containers import Container


router = APIRouter()


# Criar pagamento para o pedido
@router.post(
    "/payment",
    # dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_CREATE_PAYMENT])],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_payment(
    payment_method: str,
    # current_user: dict = Depends(get_current_user),
    controller: PaymentController = Depends(Provide[Container.payment_controller]),
):
    return controller.process_payment(payment_method)
