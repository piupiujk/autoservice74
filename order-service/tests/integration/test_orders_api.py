import pytest

from tests.conftest import http_client


def test_create_order(http_client):
    client = http_client
    response = client.post(
        "/orders",
        params={
            "user_id": 1,
            "product_id": 1
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["product_id"] == 1
    assert data["status"] == "created"


def test_get_orders(http_client):
    client = http_client
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_order_by_id(http_client):
    client = http_client
    # Сначала создаем заказ
    create_response = client.post(
        "/orders",
        params={"user_id": 1, "product_id": 1}
    )
    order_id = create_response.json()["order_id"]

    # Получаем по ID
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == order_id


def test_update_order(http_client):
    client = http_client
    # Создаем заказ
    create_response = client.post(
        "/orders",
        params={"user_id": 1, "product_id": 1}
    )
    order_id = create_response.json()["order_id"]

    # Обновляем
    update_response = client.patch(
        f"/orders/{order_id}",
        params={"status": "completed"}
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status"] == "completed"


def test_delete_order(http_client):
    client = http_client
    # Создаем заказ
    create_response = client.post(
        "/orders",
        params={"user_id": 1, "product_id": 1}
    )
    order_id = create_response.json()["order_id"]

    # Удаляем
    delete_response = client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 204

    # Проверяем, что удалено
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404
