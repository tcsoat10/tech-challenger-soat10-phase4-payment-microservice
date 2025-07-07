import traceback
import requests
from typing import Dict, Any
from config.settings import MERCADO_PAGO_ACCESS_TOKEN, MERCADO_PAGO_USER_ID, MERCADO_PAGO_POS_ID
from src.constants.payment_status import PaymentStatusEnum
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway


class MercadoPagoGateway(IPaymentProviderGateway):
    """
    Implementação do gateway de pagamento usando a API oficial do Mercado Pago.
    """
    def __init__(self):
        self.base_url = 'https://api.mercadopago.com'
        self.headers = {
            "Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

    def initiate_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma preferência de pagamento no Mercado Pago.
        :param payment_data: Dados para criar o pagamento.
        :return: Detalhes do pagamento, como QR Code e ID da transação.
        """
        payload = {
            "external_reference": payment_data.get("external_reference", ""),
            "notification_url": payment_data.get("notification_url", ""),
            "total_amount": payment_data.get("total_amount", 0.0),
            "items": payment_data.get("items", []),
            "title": payment_data.get("title", ""),
            "description": payment_data.get("description", "")
        }

        url = f"{self.base_url}/instore/orders/qr/seller/collectors/{MERCADO_PAGO_USER_ID}/pos/{MERCADO_PAGO_POS_ID}/qrs"
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code != 201:
            raise BadRequestException(f"Erro ao criar pagamento: {response.text}")

        return response.json()

    def verify_payment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica o status de um pagamento.
        :param payload: Dados do payload para verificar o pagamento.
        :return: Detalhes do status do pagamento.
        """
        try:
            if "action" in payload and payload["action"] == "payment.created":
                return {"message": payload.get("action"), "action": 'return'}

            resource = payload.get("resource")
            if not resource:
                raise BadRequestException("Payload inválido: recurso ausente.")

            if not resource.startswith('https://api.mercadolibre.com'):
                parts = resource.split('/')
                merchant_order_id = parts[-1]
                if 'merchant_order' in payload.get('topic', ''):
                    resource = f"{self.base_url}/merchant_orders/{merchant_order_id}"
                else:
                    resource = f"{self.base_url}/v1/payments/{merchant_order_id}"

            response = requests.get(resource, headers=self.headers)
            
            if response.status_code != 200:
                raise BadRequestException(f"Erro ao buscar pagamento: {response.text}")

            payment_data = response.json()
            if not payment_data:
                raise BadRequestException("Dados de pagamento não encontrados.")

            return {
                "external_reference": payment_data.get("external_reference"),
                "payment_status": payment_data.get("status"),
                "payment_method": payment_data.get("payment_method_id"),
                "transaction_amount": payment_data.get("transaction_amount"),
                "payment_date": payment_data.get("date_created"),
                "merchant_order_id": payment_data.get("merchant_order_id"),
                "payer": payment_data.get("payer"),
                "payment_type": payment_data.get("payment_type_id"),
                "last_modified": payment_data.get("date_last_updated"),
                "action": 'process'
            }
        except Exception as e:
            traceback.print_exc()
            raise BadRequestException(f"Erro ao verificar pagamento: {str(e)}")

    def status_map(self, status_name: str) -> str:
        """
        Mapeia os status de pagamento do Mercado Pago para os status internos da aplicação.
        :param status_name: Status do pagamento.
        :return: Status mapeado.
        """
        STATUS_MAP = {
            "approved": PaymentStatusEnum.PAYMENT_COMPLETED,
            "closed": PaymentStatusEnum.PAYMENT_COMPLETED,
            "opened": PaymentStatusEnum.PAYMENT_PENDING,
            "pending": PaymentStatusEnum.PAYMENT_PENDING,
            "cancelled": PaymentStatusEnum.PAYMENT_CANCELLED,
            "expired": PaymentStatusEnum.PAYMENT_CANCELLED,
            "refunded": PaymentStatusEnum.PAYMENT_REFUNDED,
            "partially_refunded": PaymentStatusEnum.PAYMENT_PARTIALLY_REFUNDED,
        }

        if status_name not in STATUS_MAP:
            # Log para identificar status desconhecidos
            print(f"Status desconhecido recebido: {status_name}")
            raise BadRequestException(f"Status de pagamento não mapeado: {status_name}")

        return STATUS_MAP[status_name]