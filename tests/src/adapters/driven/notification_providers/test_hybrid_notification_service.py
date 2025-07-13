import pytest
from unittest.mock import MagicMock
from src.adapters.driven.notification_providers.hybrid_notification_service import HybridNotificationService
from src.core.ports.notification.i_notification_service import INotificationService

@pytest.fixture
def mock_service_one():
    service = MagicMock(spec=INotificationService)
    service.name = "ServiceOne"
    return service

@pytest.fixture
def mock_service_two():
    service = MagicMock(spec=INotificationService)
    service.name = "ServiceTwo"
    return service

def test_hybrid_notification_service_is_instance_of_interface():
    assert isinstance(HybridNotificationService(), INotificationService)

def test_send_notification_first_service_succeeds(mock_service_one, mock_service_two):
    mock_service_one.send_payment_notification.return_value = True
    
    services = {"one": mock_service_one, "two": mock_service_two}
    hybrid_service = HybridNotificationService(services=services)
    
    result = hybrid_service.send_payment_notification("url", {})
    
    assert result is True
    mock_service_one.send_payment_notification.assert_called_once_with("url", {})
    mock_service_two.send_payment_notification.assert_not_called()

def test_send_notification_first_fails_second_succeeds(mock_service_one, mock_service_two):
    mock_service_one.send_payment_notification.return_value = False
    mock_service_two.send_payment_notification.return_value = True
    
    services = {"one": mock_service_one, "two": mock_service_two}
    hybrid_service = HybridNotificationService(services=services)
    
    result = hybrid_service.send_payment_notification("url", {})
    
    assert result is True
    mock_service_one.send_payment_notification.assert_called_once_with("url", {})
    mock_service_two.send_payment_notification.assert_called_once_with("url", {})

def test_send_notification_all_services_fail(mock_service_one, mock_service_two):
    mock_service_one.send_payment_notification.return_value = False
    mock_service_two.send_payment_notification.return_value = False
    
    services = {"one": mock_service_one, "two": mock_service_two}
    hybrid_service = HybridNotificationService(services=services)
    
    result = hybrid_service.send_payment_notification("url", {})
    
    assert result is False
    mock_service_one.send_payment_notification.assert_called_once_with("url", {})
    mock_service_two.send_payment_notification.assert_called_once_with("url", {})

def test_send_notification_first_raises_exception(mock_service_one, mock_service_two):
    mock_service_one.send_payment_notification.side_effect = Exception("Connection Error")
    mock_service_two.send_payment_notification.return_value = True
    
    services = {"one": mock_service_one, "two": mock_service_two}
    hybrid_service = HybridNotificationService(services=services)
    
    result = hybrid_service.send_payment_notification("url", {})
    
    assert result is True
    mock_service_one.send_payment_notification.assert_called_once_with("url", {})
    mock_service_two.send_payment_notification.assert_called_once_with("url", {})

def test_send_notification_with_no_services():
    hybrid_service = HybridNotificationService(services={})
    result = hybrid_service.send_payment_notification("url", {})
    assert result is False
