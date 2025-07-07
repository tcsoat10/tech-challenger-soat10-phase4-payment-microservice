from pydantic import BaseModel, ConfigDict, Field


class UpdatePaymentDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    payment_method_id: int = Field(..., gt=0)
    payment_status_id: int = Field(..., gt=0)