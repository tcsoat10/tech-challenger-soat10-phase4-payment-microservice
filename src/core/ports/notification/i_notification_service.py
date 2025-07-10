from abc import ABC, abstractmethod
from typing import Dict, Any

class INotificationService(ABC):
    """Interface para serviços de notificação"""
    
    @abstractmethod
    def send_payment_notification(self, notification_url: str, payment_data: Dict[str, Any]) -> bool:
        """
        Envia notificação de pagamento para a URL especificada
        
        :param notification_url: URL para enviar a notificação
        :param payment_data: Dados do pagamento para enviar
        :return: True se enviado com sucesso, False caso contrário
        """
        pass
