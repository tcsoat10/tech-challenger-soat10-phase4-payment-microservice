import logging
import os
from typing import Dict, Any
from celery import Task
import requests
from config.celery_config import celery_app
from src.core.ports.notification.i_notification_service import INotificationService

logger = logging.getLogger(__name__)

class CeleryNotificationService(INotificationService):
    """Implementação puramente assíncrona via Celery"""
        
    def send_payment_notification(self, notification_url: str, payment_data: Dict[str, Any]) -> bool:
        """
        Envia notificação assíncrona de notificação de pagamento.
        
        :param notification_url: URL para enviar a notificação
        :param payment_data: Dados do pagamento
        :return: True se enviado para fila com sucesso
        """
        try:
            logger.info("Enviando notificação para fila assíncrona...")
            task = send_payment_notification_task.delay(notification_url, payment_data)
            logger.info(f"Task de notificação enviada para fila assíncrona. Task ID: {task.id}")
            return True
            
        except Exception as e:
            logger.error(f"Falha ao enviar task para fila assíncrona. Erro: {e}")
            return False


class NotificationTask(Task):
    """Task customizada com retry automático"""
    autoretry_for = (Exception,)
    retry_kwargs = {
        'max_retries': int(os.getenv('CELERY_NOTIFICATION_MAX_RETRIES', 3)),
        'countdown': int(os.getenv('CELERY_NOTIFICATION_RETRY_DELAY_SECONDS', 5))
    }
    retry_backoff = True
    retry_jitter = False


@celery_app.task(bind=True, base=NotificationTask, name='send_payment_notification_task')
def send_payment_notification_task(self, notification_url: str, payment_data: Dict[str, Any]) -> bool:
    """
    Task Celery para envio assíncrono de notificação de pagamento
    
    :param notification_url: URL para enviar a notificação
    :param payment_data: Dados do pagamento
    :return: True se enviado com sucesso
    """
    logger.info(f"Executando task assíncrona de notificação. Task ID: {self.request.id}")
    
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
    
    logger.info(f"Enviando notificação HTTP para {notification_url}")
    
    try:
        response = requests.post(
            notification_url,
            json=payload,
            headers=headers,
            timeout=int(os.getenv('NOTIFICATION_TIMEOUT_SECONDS', 30))
        )
        response.raise_for_status()
        
        logger.info(f"Notificação assíncrona enviada com sucesso. Task ID: {self.request.id}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na task assíncrona {self.request.id}: {e}")
        raise self.retry(exc=e)