from pydantic import BaseModel, ConfigDict, Field


class CreatePaymentDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    title: str = Field(
        ...,
        description="Título do pagamento",
        example="Pagamento do pedido #12345",
    )
    description: str = Field(
        default="Pagamento do pedido",
        description="Descrição do pagamento",
        example="Pagamento do pedido #12345",
    )
    payment_method: str = Field(
        ...,
        description="Método de pagamento utilizado para o pagamento do pedido",
        example="qr_code",
    )
    total_amount: float = Field(
        ...,
        description="Valor total do pagamento",
        example=100.0,
    )
    currency: str = Field(
        ...,
        description="Moeda utilizada no pagamento",
        example="BRL",
    )
    notification_url: str = Field(
        ...,
        description="URL de callback para notificações de pagamento",
        example="https://example.com/callback",
    )
class Item(BaseModel):
    name: str = Field(..., description="Nome do item", example="item1")
    description: str = Field(..., description="Descrição do item", example="Item 1")
    category: str = Field(..., description="Categoria do item", example="hamburgers")
    quantity: int = Field(..., description="Quantidade do item", example=1)
    unit_price: float = Field(..., description="Preço unitário do item", example=50.0)

class Customer(BaseModel):
    name: str = Field(..., description="Nome do cliente", example="João da Silva")
    email: str = Field(..., description="Email do cliente", example="joao@example.com")

class CreatePaymentDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    title: str = Field(
        ...,
        description="Título do pagamento",
        example="Pagamento do pedido #12345",
    )
    description: str = Field(
        default="Pagamento do pedido",
        description="Descrição do pagamento",
        example="Pagamento do pedido #12345",
    )
    payment_method: str = Field(
        ...,
        description="Método de pagamento utilizado para o pagamento do pedido",
        example="qr_code",
    )
    total_amount: float = Field(
        ...,
        description="Valor total do pagamento",
        example=100.0,
    )
    currency: str = Field(
        ...,
        description="Moeda utilizada no pagamento",
        example="BRL",
    )
    notification_url: str = Field(
        ...,
        description="URL de callback para notificações de pagamento",
        example="https://example.com/callback",
    )
    items: list[Item] = Field(
        ...,
        description="Itens do pedido",
        example=[
            {
                "name": "item1",
                "description": "Item 1",
                "category": "hamburgers",
                "quantity": 1,
                "unit_price": 50.0
            },
            {
                "name": "item2",
                "description": "Item 2",
                "category": "drinks",
                "quantity": 1,
                "unit_price": 50.0
            }
        ]
    )
    customer: dict = Field(
        ...,
        description="Informações do cliente",
        example={
            "name": "João da Silva",
            "email": ""
        }
    )
