import unittest
from unittest.mock import patch, MagicMock
from src.constants.payment_status import PaymentStatusEnum
from src.adapters.driven.payment_providers.mercado_pago_gateway import MercadoPagoGateway
from src.core.exceptions.bad_request_exception import BadRequestException

class TestMercadoPagoGateway(unittest.TestCase):

    def setUp(self):
        self.gateway = MercadoPagoGateway()

    @patch('requests.post')
    def test_initiate_payment_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"qr_data": "qr_code_link", "in_store_order_id": "transaction_id"}
        mock_post.return_value = mock_response

        payment_data = {
            "external_reference": "order-1-uuid",
            "notification_url": "http://example.com/webhook",
            "total_amount": 100.0,
            "items": [],
            "title": "Order 1",
            "description": "Order 1 description"
        }

        result = self.gateway.initiate_payment(payment_data)
        self.assertEqual(result["qr_data"], "qr_code_link")
        self.assertEqual(result["in_store_order_id"], "transaction_id")

    @patch('requests.post')
    def test_initiate_payment_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Error"
        mock_post.return_value = mock_response

        payment_data = {
            "external_reference": "order-1-uuid",
            "notification_url": "http://example.com/webhook",
            "total_amount": 100.0,
            "items": [],
            "title": "Order 1",
            "description": "Order 1 description"
        }

        with self.assertRaises(BadRequestException):
            self.gateway.initiate_payment(payment_data)

    @patch('requests.get')
    def test_verify_payment_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "external_reference": "order-1-uuid",
            "status": "approved",
            "payment_method_id": "credit_card",
            "transaction_amount": 100.0,
            "date_created": "2023-01-01T00:00:00Z",
            "merchant_order_id": "12345",
            "payer": {},
            "payment_type_id": "credit_card",
            "date_last_updated": "2023-01-01T00:00:00Z"
        }
        mock_get.return_value = mock_response

        payload = {"resource": "https://api.mercadopago.com/v1/payments/12345"}
        result = self.gateway.verify_payment(payload)
        self.assertEqual(result["external_reference"], "order-1-uuid")
        self.assertEqual(result["payment_status"], "approved")

    @patch('requests.get')
    def test_verify_payment_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Error"
        mock_get.return_value = mock_response

        payload = {"resource": "https://api.mercadopago.com/v1/payments/12345"}
        with self.assertRaises(BadRequestException):
            self.gateway.verify_payment(payload)

    @patch('requests.get')
    def test_verify_payment_invalid_resource(self, mock_get):
        payload = {"resource": "invalid_resource"}
        with self.assertRaises(BadRequestException):
            self.gateway.verify_payment(payload)

    @patch('requests.get')
    def test_verify_payment_no_resource(self, mock_get):
        payload = {}
        with self.assertRaises(BadRequestException):
            self.gateway.verify_payment(payload)

    def test_status_map(self):
        self.assertEqual(self.gateway.status_map("approved"), PaymentStatusEnum.PAYMENT_COMPLETED)
        self.assertEqual(self.gateway.status_map("pending"), PaymentStatusEnum.PAYMENT_PENDING)
        self.assertEqual(self.gateway.status_map("cancelled"), PaymentStatusEnum.PAYMENT_CANCELLED)

        with self.assertRaises(BadRequestException):
            self.gateway.status_map("unknown_status")

    def test_status_map_unknown_status(self):
        with self.assertRaises(BadRequestException):
            self.gateway.status_map("unknown_status")

