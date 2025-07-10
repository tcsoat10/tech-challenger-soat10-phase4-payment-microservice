from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from starlette.requests import ClientDisconnect
import logging

from src.core.containers import Container
from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
from src.adapters.driver.api.v1.decorators.bypass_auth import bypass_auth

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/webhook/payment", include_in_schema=False)
@bypass_auth()
@inject
async def webhook(request: Request, payment_controller: PaymentController = Depends(Provide[Container.payment_controller])):
    """
    Endpoint para processar webhooks enviados pelo payment provider.
    """
    try:
        # Verificar se há body na requisição
        try:
            body = await request.body()
            if not body:
                logger.warning("Webhook recebido sem body")
                return JSONResponse(content={"message": "Webhook sem conteúdo processado"}, status_code=200)
        except ClientDisconnect:
            logger.warning("Cliente desconectou durante leitura do body")
            return JSONResponse(content={"message": "Cliente desconectou"}, status_code=200)
    
        try:
            payload = await request.json()
        except ClientDisconnect:
            logger.warning("Cliente desconectou durante parse do JSON")
            return JSONResponse(content={"message": "Cliente desconectou"}, status_code=200)
        except Exception as e:
            logger.error(f"Erro ao fazer parse do JSON do webhook: {e}")
            return JSONResponse(content={"error": "Invalid JSON payload"}, status_code=400)

        logger.info(f"Webhook recebido: {payload}")
        payment_controller.payment_provider_webhook(payload)
        return JSONResponse(content={"message": "Webhook processado com sucesso!"}, status_code=200)
        
    except ClientDisconnect:
        logger.warning("Cliente desconectou durante processamento")
        return JSONResponse(content={"message": "Cliente desconectou"}, status_code=200)
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return JSONResponse(content={"error": "Erro interno do servidor"}, status_code=500)
