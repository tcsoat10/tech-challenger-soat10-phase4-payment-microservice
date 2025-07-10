from dependency_injector import containers, providers

from src.adapters.driven.notification_providers.http_notification_service import HttpNotificationService
from src.adapters.driven.notification_providers.celery_notification_service import CeleryNotificationService
from src.adapters.driven.notification_providers.hybrid_notification_service import HybridNotificationService
from config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.payment_status_repository import PaymentStatusRepository
from src.adapters.driver.api.v1.controllers.payment_status_controller import PaymentStatusController
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.adapters.driver.api.v1.controllers.payment_method_controller import PaymentMethodController
from src.adapters.driven.repositories.payment_repository import PaymentRepository
from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
from src.adapters.driven.payment_providers.mercado_pago_gateway import MercadoPagoGateway


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.adapters.driver.api.v1.controllers.payment_status_controller",
        "src.adapters.driver.api.v1.routes.payment_status_routes",
        "src.adapters.driver.api.v1.controllers.payment_method_controller",
        "src.adapters.driver.api.v1.routes.payment_method_routes",
        "src.adapters.driver.api.v1.controllers.payment_controller",
        "src.adapters.driver.api.v1.routes.payment_routes",
        "src.adapters.driver.api.v1.routes.webhook_routes"
    ])
    
    identity_map = providers.Singleton(IdentityMap)

    # MongoDB connection context - no longer a session but a connection context
    db_connection = providers.Resource(get_db)

    # Payment Status components
    payment_status_gateway = providers.Factory(PaymentStatusRepository)
    payment_status_controller = providers.Factory(
        PaymentStatusController, payment_status_gateway=payment_status_gateway
    )

    # Payment Method components
    payment_method_gateway = providers.Factory(PaymentMethodRepository)
    payment_method_controller = providers.Factory(
        PaymentMethodController, payment_method_gateway=payment_method_gateway
    )

    # Notification Service Provider
    http_notification_service = providers.Factory(HttpNotificationService)
    celery_notification_service = providers.Factory(CeleryNotificationService)    
    notification_services = providers.Dict({
        "http": http_notification_service,
        "celery": celery_notification_service
    })
    notification_service = providers.Factory(
        HybridNotificationService, services=notification_services
    )

    # Payment Provider
    payment_provider_gateway = providers.Factory(MercadoPagoGateway)

    # Payment components
    payment_gateway = providers.Factory(PaymentRepository)
    payment_controller = providers.Factory(
        PaymentController,
        payment_gateway=payment_gateway,
        payment_provider_gateway=payment_provider_gateway,
        payment_status_gateway=payment_status_gateway,
        payment_method_gateway=payment_method_gateway,
        notification_service=notification_service
    )
