from datetime import datetime
from bson import ObjectId
from fastapi import status

import pytest

from src.core.exceptions.utils import ErrorCode
from tests.factories.payment_method_factory import PaymentMethodFactory

@pytest.mark.parametrize("payload", [
    {"name": "Pix", "description": "Pay with Pix"},
    {"name": "Credit Card", "description": "Pay with credit card"},
])
def test_create_payment_method_success(client, payload):
    response = client.post("/api/v1/payment-methods", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

def test_create_payment_method_duplicate_name_and_return_error(client):
    PaymentMethodFactory(name="Pix", description="Pay with Pix")

    payload = {"name": "Pix", "description": "Pay with Pix"}
    response = client.post("/api/v1/payment-methods", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Payment method already exists.',
            'details': None,
        }
    }

def test_reactivate_payment_method_and_return_success(client):
    PaymentMethodFactory(name="Pix", description="Pay with Pix", inactivated_at=datetime.now())

    payload = {"name": "Pix", "description": "Pay with Pix"}
    response = client.post("/api/v1/payment-methods", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

def test_send_unexpected_param_to_create_payment_method_and_return_error(client):
    payload = {"name": "Pix", "description": "Pay with Pix", "unexpected_param": "123"}
    response = client.post("/api/v1/payment-methods", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_payment_method_name_great_than_limit_and_return_error(client):
    payload = {"name": "c"*101, "description": "Pay with Pix"}
    response = client.post("/api/v1/payment-methods", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_payment_method_by_name_and_return_success(client):
    PaymentMethodFactory(name="Pix", description="Pay with Pix")
    credit_card = PaymentMethodFactory(name="Credit Card", description="Pay with credit card")

    response = client.get("/api/v1/payment-methods/Credit Card/name")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(credit_card.id),
        "name": "Credit Card",
        "description": "Pay with credit card"
    }

def test_get_payment_method_by_id_and_return_success(client):
    PaymentMethodFactory(name="Pix", description="Pay with Pix")
    credit_card = PaymentMethodFactory(name="Credit Card", description="Pay with credit card")

    response = client.get(f"/api/v1/payment-methods/{credit_card.id}/id")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(credit_card.id),
        "name": "Credit Card",
        "description": "Pay with credit card"
   }

def test_get_all_payment_methods_and_return_success(client):
    pix = PaymentMethodFactory(name="Pix", description="Pay with Pix")
    credit_card = PaymentMethodFactory(name="Credit Card", description="Pay with credit card")

    response = client.get("/api/v1/payment-methods")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json() == [
        {
            "id": str(pix.id),
            "name": "Pix",
            "description": "Pay with Pix"
        },
        {
            "id": str(credit_card.id),
            "name": "Credit Card",
            "description": "Pay with credit card"
        }
    ]

def test_update_payment_method_and_return_success(client):
    pix = PaymentMethodFactory(name="Pix", description="Pay with Pix")

    payload = {"id": str(pix.id), "name": "Credit Card", "description": "Pay with credit card"}
    response = client.put(f"/api/v1/payment-methods/{pix.id}", json=payload)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == str(pix.id)
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

def test_update_payment_method_name_great_than_limit_and_return_error(client):
    pix = PaymentMethodFactory(name="Pix", description="Pay with Pix")

    payload = {"name": "c"*101, "description": "Pay with credit card"}
    response = client.put(f"/api/v1/payment-methods/{pix.id}", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_update_payment_method_duplicate_name_and_return_error(client):
    pix = PaymentMethodFactory(name="Pix", description="Pay with Pix")
    credit_card = PaymentMethodFactory(name="Credit Card", description="Pay with credit card")

    payload = {"id": str(credit_card.id), "name": "Credit Card", "description": "Pay with credit card"}
    response = client.put(f"/api/v1/payment-methods/{pix.id}", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Payment method already exists.',
            'details': None,
        }
    }

def test_delete_payment_method_and_return_success(client):
    pix = PaymentMethodFactory(name="Pix", description="Pay with Pix")

    response = client.delete(f"/api/v1/payment-methods/{pix.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_payment_method_not_found_and_return_error(client):
    response = client.delete(f"/api/v1/payment-methods/{ObjectId()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Payment method not found.',
            'details': None,
        }
    }
