from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
from src.adapters.driver.api.v1.decorators.bypass_auth import bypass_auth


router = APIRouter()
    

@router.post("/webhook/payment", include_in_schema=False)
@bypass_auth()
@inject
async def webhook(request: Request, payment_controller: PaymentController = Depends(Provide[Container.payment_controller])):
    """
    Endpoint para processar webhooks enviados pelo payment provider.
    """
    payload = await request.json()

    payment_controller.payment_provider_webhook(payload)
    return JSONResponse(content={"message": "Webhook processado com sucesso!"}, status_code=200)
