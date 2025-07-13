import os
import pytest
from fastapi.testclient import TestClient
from typing import Generator
import mongomock
from mongoengine import connect, disconnect
from unittest.mock import patch

from src.app import app
from src.core.containers import Container


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""
    # Set test environment variables
    os.environ['MONGO_DB'] = 'test_payment_service'
    os.environ['MONGO_HOST'] = 'localhost'
    os.environ['MONGO_PORT'] = '27017'
    os.environ['MONGO_USER'] = ''
    os.environ['MONGO_PASSWORD'] = ''

    # Celery config celery for tests
    os.environ['CELERY_TASK_ALWAYS_EAGER'] = 'True'
    os.environ['CELERY_BROKER_URL'] = 'memory://'
    os.environ['CELERY_RESULT_BACKEND'] = 'rpc://'
    os.environ['CELERY_NOTIFICATION_MAX_RETRIES'] = '2'
    os.environ['CELERY_NOTIFICATION_RETRY_DELAY_SECONDS'] = '0'

    yield
    # Cleanup after tests
    try:
        disconnect(alias='test')
        disconnect(alias='default')
    except Exception:
        pass


@pytest.fixture(scope="function")
def mongo_db():
    """
    Fixture para configurar um banco de dados MongoDB mock para testes.
    """
    try:
        disconnect(alias='test')
    except Exception:
        pass

    connect(
        db='test_payment_service',
        host='localhost',
        port=27017,
        mongo_client_class=mongomock.MongoClient,
        alias='test'
    )
    
    yield mongomock.MongoClient('localhost', 27017)

    try:
        disconnect(alias='test')
    except Exception:
        pass


@pytest.fixture(scope="function")
def client(mongo_db) -> Generator[TestClient, None, None]:
    """
    Cria um cliente de teste para a aplicação.
    """
    # Mock the connect_db function to use test alias
    with patch('config.database.connect_db') as mock_connect:
        with patch('config.database.disconnect_db') as mock_disconnect:
            mock_connect.return_value = None
            mock_disconnect.return_value = None
            
            with TestClient(app) as test_client:
                yield test_client


@pytest.fixture(scope="function")
def container(mongo_db) -> Generator[Container, None, None]:
    """
    Cria um container de dependências para testes.
    """
    container = Container()
    container.wire(modules=[
        "tests.src.adapters.driven.repositories.test_payment_method_repository",
        "tests.src.adapters.driven.repositories.test_payment_status_repository",
        "tests.src.adapters.driven.repositories.test_payment_repository",
    ])
    yield container
    container.unwire()


@pytest.fixture(autouse=True)
def clean_database(mongo_db):
    """
    Limpa o banco de dados antes e depois de cada teste.
    """
    # Clean before test
    try:
        from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel
        from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel
        from src.adapters.driven.repositories.models.payment_model import PaymentModel
        
        # Switch to test database
        PaymentMethodModel._get_db = lambda: mongo_db['test_payment_service']
        PaymentStatusModel._get_db = lambda: mongo_db['test_payment_service']
        PaymentModel._get_db = lambda: mongo_db['test_payment_service']
        
        PaymentMethodModel.objects.delete()
        PaymentStatusModel.objects.delete()
        PaymentModel.objects.delete()
    except Exception as e:
        print(f"Error cleaning database: {e}")
    
    yield
    
    # Clean after test
    try:
        PaymentMethodModel.objects.delete()
        PaymentStatusModel.objects.delete()  
        PaymentModel.objects.delete()
    except Exception as e:
        print(f"Error cleaning database after test: {e}")
