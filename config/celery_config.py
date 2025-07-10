import os
from celery import Celery
from kombu import Queue

# Configuração do Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'payment-microservice-redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

# URL de conexão do Redis
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

print(f"Celery conectando no Redis: {REDIS_URL}")

celery_app = Celery(
    'payment_microservice',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['src.adapters.driven.notification_providers.celery_notification_service']
)

# Configurações do Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60, # 30 minutos
    task_soft_time_limit=25 * 60, # 25 minutos
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    task_routes={
        'send_payment_notification_task': {
            'queue': 'notifications'
        },
    },
    task_default_queue='default',
    task_queues=(
        Queue('default'),
        Queue('notifications'),
    ),
    task_acks_late=True,
    worker_send_task_events=True,
    task_send_sent_event=True,
    # Configurações específicas para Flower
    worker_hijack_root_logger=False,
    worker_log_color=False,
    task_result_expires=3600,  # 1 hora
    result_expires=3600,
    # Configuração de retry para conexão
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
)

celery_app.autodiscover_tasks()
