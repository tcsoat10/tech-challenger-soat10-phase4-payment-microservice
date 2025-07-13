import os
import pytest
import requests
from unittest.mock import patch, MagicMock
from src.adapters.driven.notification_providers.http_notification_service import HttpNotificationService
from src.core.ports.notification.i_notification_service import INotificationService
from tenacity import retry, stop_after_attempt, wait_fixed

@pytest.fixture
def notification_service():
    service = HttpNotificationService(timeout=1)
    service.max_retries = 3
    service.retry_delay = 0

    service.send_payment_notification = retry(
        stop=stop_after_attempt(service.max_retries),
        wait=wait_fixed(service.retry_delay),
        reraise=True
    )(service._send_notification)
    
    return service

@pytest.fixture(autouse=True)
def mock_tenacity_retry():
    def no_retry_decorator(func):
        return func

    dummy_retry = MagicMock()
    dummy_retry.side_effect = lambda *args, **kwargs: no_retry_decorator

    with patch('src.adapters.driven.notification_providers.http_notification_service.retry', dummy_retry):
        yield

def test_http_notification_service_is_instance_of_interface(notification_service):
    assert isinstance(notification_service, INotificationService)

@patch('requests.post')
def test_send_payment_notification_success(mock_post, notification_service):
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

    result = notification_service.send_payment_notification(notification_url, payment_data)

    assert result is True
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args.args[0] == notification_url
    assert call_args.kwargs['json']['event'] == 'payment.completed'
    assert call_args.kwargs['json']['payment_id'] == payment_data['payment_id']

@patch('requests.post')
def test_send_payment_notification_http_error_with_retries(mock_post, notification_service):
    mock_response = mock_post.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
    
    notification_url = "http://test.com/notify"
    payment_data = {"payment_id": "123"}

    with pytest.raises(requests.exceptions.HTTPError):
        notification_service.send_payment_notification(notification_url, payment_data)

    assert mock_post.call_count == notification_service.max_retries

@patch('requests.post')
def test_send_payment_notification_timeout_with_retries(mock_post, notification_service):
    mock_post.side_effect = requests.exceptions.ConnectTimeout("Timeout")

    notification_url = "http://test.com/notify"
    payment_data = {"payment_id": "123"}

    with pytest.raises(requests.exceptions.ConnectTimeout):
        notification_service.send_payment_notification(notification_url, payment_data)

    assert mock_post.call_count == notification_service.max_retries

@patch('requests.post')
def test_send_payment_notification_success_after_retry(mock_post, notification_service):
    mock_response_fail = requests.Response()
    mock_response_fail.status_code = 500
    mock_response_fail.reason = "Internal Server Error"
    mock_response_fail.raise_for_status = lambda: mock_response_fail.reason

    mock_response_success = requests.Response()
    mock_response_success.status_code = 200
    mock_response_success.reason = "OK"
    mock_response_success.raise_for_status = lambda: None


    mock_post.side_effect = [
        requests.exceptions.RequestException("Error"),
        mock_response_success
    ]

    notification_url = "http://test.com/notify"
    payment_data = {"payment_id": "123"}

    result = notification_service.send_payment_notification(notification_url, payment_data)

    assert result is True
    assert mock_post.call_count == 2
