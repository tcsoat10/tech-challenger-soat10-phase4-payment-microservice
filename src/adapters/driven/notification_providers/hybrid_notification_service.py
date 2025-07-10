import logging
from typing import Dict, Any
from src.core.ports.notification.i_notification_service import INotificationService

logger = logging.getLogger(__name__)

class HybridNotificationService(INotificationService):
    """
    Serviço híbrido que coordena notificações síncronas e assíncronas
    Respeitando os princípios da Clean Architecture
    """
    
    def __init__(self, services: Dict[str, INotificationService] = {}):
        self._services = services
    
    def send_payment_notification(self, notification_url: str, payment_data: Dict[str, Any]) -> bool:
        """
        Envia notificação usando estratégia para multiplos serviços de notificação.
        
        :param notification_url: URL para enviar a notificação
        :param payment_data: Dados do pagamento
        :return: True se enviado com sucesso
        """
        
        for service_name, service in self._services.items():
            try:
                logger.info(f"Tentando enviar notificação via {service_name}...")
                result = service.send_payment_notification(notification_url, payment_data)
                
                if result:
                    logger.info(f"Notificação enviada com sucesso via {service_name}")
                    return True
                
            except NotImplementedError as e:
                logger.warning(f"Serviço {service_name} não implementado: {e}")
                continue  # Pula para o próximo serviço
            except Exception as e:
                logger.warning(f"Falha ao enviar notificação via {service_name}: {e}")
                continue  # Pula para o próximo serviço
        
        logger.error("Todos os serviços de notificação falharam")
        return False