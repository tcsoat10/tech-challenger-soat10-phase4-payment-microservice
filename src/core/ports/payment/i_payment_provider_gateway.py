from abc import ABC, abstractmethod
from typing import Dict, Any


class IPaymentProviderGateway(ABC):
    """
    Interface para gateways de pagamento. Define os métodos necessários para integrar diferentes
    provedores de pagamento, como Mercado Pago ou gateways simulados.
    """

    @abstractmethod
    def initiate_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inicia um pagamento e retorna os dados necessários, como QR Code ou links de pagamento.

        :param payment_data: Dados necessários para criar o pagamento (ex.: valor, descrição, e-mail do cliente).
        :return: Dicionário contendo os dados do pagamento, como links ou identificadores únicos.
        """
        pass

    @abstractmethod
    def verify_payment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica o status de um pagamento pelo ID fornecido.

        :param payment_id: ID único do pagamento no gateway (ex.: external_reference).
        :return: Dicionário contendo o status atualizado do pagamento.
        """
        pass

    @abstractmethod
    def status_map(self, status_name: str) -> str:
        """
        Mapeia o status retornado pelo gateway para o status interno do sistema.

        :param status_name: Nome do status retornado pelo gateway.
        :return: Nome do status interno correspondente.
        """
        pass
