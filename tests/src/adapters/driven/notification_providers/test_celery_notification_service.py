import pytest
from unittest.mock import patch, MagicMock
import requests
from src.adapters.driven.notification_providers.celery_notification_service import (
    CeleryNotificationService,
    send_payment_notification_task
)
from src.core.ports.notification.i_notification_service import INotificationService

@pytest.fixture
def celery_notification_service():
    return CeleryNotificationService()

def test_celery_notification_service_is_instance_of_interface(celery_notification_service):
    assert isinstance(celery_notification_service, INotificationService)

@patch('src.adapters.driven.notification_providers.celery_notification_service.send_payment_notification_task.delay')
def test_send_payment_notification_success(mock_delay, celery_notification_service):
    mock_delay.return_value = MagicMock(id="test_task_id")
    
    notification_url = "http://test.com/notify"
    payment_data = {"payment_id": "123"}

    result = celery_notification_service.send_payment_notification(notification_url, payment_data)

    assert result is True
    mock_delay.assert_called_once_with(notification_url, payment_data)

@patch('src.adapters.driven.notification_providers.celery_notification_service.send_payment_notification_task.delay')
def test_send_payment_notification_failure(mock_delay, celery_notification_service):
    mock_delay.side_effect = Exception("Queueing error")
    
    notification_url = "http://test.com/notify"
    payment_data = {"payment_id": "123"}

    result = celery_notification_service.send_payment_notification(notification_url, payment_data)

    assert result is False
    mock_delay.assert_called_once_with(notification_url, payment_data)

@patch('requests.post')
def test_send_payment_notification_task_success(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    notification_url = "http://test.com/notify"
    payment_data = {
        "payment_id": "123",
        "external_reference": "456",
        "amount": 100.0,
        "status": "approved",
        "transaction_id": "txn_123",
        "timestamp": "2025-07-11T12:00:00Z"
    }

    result = send_payment_notification_task(notification_url, payment_data)

    assert result is True
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args.args[0] == notification_url
    assert call_args.kwargs['json']['event'] == 'payment.completed'

@patch('requests.post')
def test_send_payment_notification_task_http_error_raises_exception(mock_post):
    original_exception = requests.exceptions.RequestException("HTTP Error")
    mock_post.side_effect = original_exception

    notification_url = "http://test.com/notify"
    payment_data = {"payment_id": "123"}

    with pytest.raises(requests.exceptions.RequestException) as excinfo:
        send_payment_notification_task(notification_url, payment_data)

    mock_post.assert_called_once()
    assert excinfo.value is original_exception
