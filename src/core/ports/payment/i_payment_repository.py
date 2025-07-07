from abc import ABC, abstractmethod

from src.core.domain.entities.payment import Payment


class IPaymentRepository(ABC):
    """
    Interface para o repositório de pagamentos, responsável pela interação com a tabela `payments`.
    """

    @abstractmethod
    def create_payment(self, payment: Payment) -> int:
        """
        Cria um novo pagamento na tabela `payments`.
        
        :param payment: Instância do pagamento a ser criado.
        :return: ID do pagamento criado.
        """
        pass

    @abstractmethod
    def update_payment_status(self, payment: Payment, status_id: int) -> None:
        """
        Atualiza o status de um pagamento na tabela `payments`.
        
        :param payment: Instância do pagamento a ser atualizado.
        :param status_id: Novo ID do status do pagamento.
        """
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: int) -> Payment:
        """
        Recupera os detalhes de um pagamento pelo ID.
        
        :param payment_id: ID do pagamento.
        :return: Dicionário contendo os detalhes do pagamento.
        """
        pass

    @abstractmethod
    def get_payment_by_reference(self, external_reference: str) -> Payment:
        """
        Recupera os detalhes de um pagamento pela referência externa.
        
        :param external_reference: Referência externa do pagamento.
        :return: Dicionário contendo os detalhes do pagamento.
        """
        pass
