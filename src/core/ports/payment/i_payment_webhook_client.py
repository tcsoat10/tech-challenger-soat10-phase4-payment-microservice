from abc import ABC, abstractmethod
from typing import Dict, Any


class IPaymentWebhookClient(ABC):
    """
    Interface para o cliente de webhook, responsável por processar os eventos enviados pelos gateways de pagamento.
    """

    @abstractmethod
    def process_webhook(self, payload: Dict[str, Any]) -> None:
        """
        Processa o payload enviado pelo gateway no webhook.

        :param payload: Dados enviados pelo gateway, contendo informações sobre o evento do pagamento.
        """
        pass
