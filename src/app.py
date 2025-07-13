from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.containers import Container
from src.adapters.driver.api.v1.middleware.identity_map_middleware import IdentityMapMiddleware
from src.adapters.driver.api.v1.middleware.custom_error_middleware import CustomErrorMiddleware
from src.adapters.driver.api.v1.routes.health_check import router as health_check_router
from src.adapters.driver.api.v1.routes.payment_method_routes import router as payment_method_routes
from src.adapters.driver.api.v1.routes.payment_status_routes import router as payment_status_routes
from src.adapters.driver.api.v1.routes.payment_routes import router as payment_routes
from src.adapters.driver.api.v1.routes.webhook_routes import router as webhook_routes
from src.adapters.driver.api.v1.middleware.api_key_middleware import ApiKeyMiddleware
from config.database import connect_db, disconnect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_db()
    yield
    disconnect_db()

app = FastAPI(
    title="Tech Challenger SOAT10 - FIAP",
    lifespan=lifespan,
    description="Microserviço de Pagamentos para o Tech Challenger SOAT10 da FIAP",
)

# Inicializando o container de dependências
container = Container()
app.container = container

app.add_middleware(ApiKeyMiddleware)
app.add_middleware(CustomErrorMiddleware)
app.add_middleware(IdentityMapMiddleware)

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix="/api/v1")
app.include_router(payment_routes, prefix="/api/v1", tags=["payment"])
app.include_router(payment_method_routes, prefix="/api/v1", tags=["payment-methods"])
app.include_router(payment_status_routes, prefix="/api/v1", tags=["payment-status"])
app.include_router(webhook_routes, prefix="/api/v1", tags=["webhooks"])
