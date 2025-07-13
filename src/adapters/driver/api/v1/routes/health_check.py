from src.schemas.health_check_schema import HealthCheckSchemaOut
from src.application.usecases.health_check_usecase.health_check_usecase import HealthCheckUseCase
from fastapi import APIRouter, status
from src.adapters.driver.api.v1.decorators.bypass_auth import bypass_auth

router = APIRouter()

@router.get("/health", response_model=HealthCheckSchemaOut, status_code=status.HTTP_200_OK)
@bypass_auth()
async def health_check():
    return HealthCheckUseCase().execute()
