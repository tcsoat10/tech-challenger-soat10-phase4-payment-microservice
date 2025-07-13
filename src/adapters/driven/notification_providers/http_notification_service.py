import requests
import logging
import os
from typing import Dict, Any
from src.core.ports.notification.i_notification_service import INotificationService
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log

logger = logging.getLogger(__name__)

class HttpNotificationService(INotificationService):
    """Implementação de notificação via HTTP"""

    MAX_RETRIES = int(os.getenv('NOTIFICATION_MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('NOTIFICATION_RETRY_DELAY_SECONDS', 5))
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_fixed(RETRY_DELAY),
        before_sleep=before_sleep_log(logger, logging.INFO),
        reraise=True
    )
    def send_payment_notification(self, notification_url: str, payment_data: Dict[str, Any]) -> bool:
        """
        Envia notificação HTTP para a URL especificada
        
        :param notification_url: URL para enviar a notificação
        :param payment_data: Dados do pagamento
        :return: True se enviado com sucesso
        """
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Payment-Microservice/1.0'
        }
        
        payload = {
            'event': 'payment.completed',
            'payment_id': payment_data.get('payment_id'),
            'external_reference': payment_data.get('external_reference'),
            'amount': payment_data.get('amount'),
            'status': payment_data.get('status'),
            'transaction_id': payment_data.get('transaction_id'),
            'timestamp': payment_data.get('timestamp')
        }
        
        logger.info(f"Enviando notificação para {notification_url}")
        
        try:
            response = requests.post(
                notification_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            logger.info(f"Notificação enviada com sucesso para {notification_url}")
            return True
        except requests.exceptions.RequestException as e:
            logger.warning(f"Falha ao enviar notificação para {notification_url}. Erro: {e}. Tentando novamente...")
            raise
