import pytest
import json
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from http import HTTPStatus
from unittest.mock import Mock, AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from modules.core.config import dependencies
from modules.customer.infrastructure.http.controller.customer_controller import router, create_customer
from modules.customer.application.service.customer_service import CustomerService
from modules.customer.domain.entity.customer import Customer, CustomerUp
from modules.customer.domain.entity.customer_filtered import CustomerFiltered

# Mock data
MOCK_TOKEN = "Bearer valid_token"
MOCK_CUSTOMER_ID = "123-abc"
MOCK_CUSTOMER = Customer(
    name="Joao",
    email="joao@test.com"
)
MOCK_CUSTOMER_UPDATE = CustomerUp(
    name="Joao Up",
    email="joaodated@test.com"
)

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
def mock_customer_service():
    return Mock(spec=CustomerService)

@pytest.fixture
def client(app, mock_customer_service):
    app.dependency_overrides[CustomerService] = lambda: mock_customer_service
    return TestClient(app)

class TestCustomerController:
    def test_get_customers_success(self, client, mock_customer_service):
        mock_paginated_response = Mock()
        mock_paginated_response.to_dict.return_value = {
            "items": [],
            "total": 0,
            "page": 1
        }
        mock_customer_service.get_all_paginated = AsyncMock(return_value=mock_paginated_response)

        response = client.get(
            "/api/customer",
            headers={"Authorization": MOCK_TOKEN}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"items": [], "total": 0, "page": 1}
        mock_customer_service.get_all_paginated.assert_called_once_with(1)

    def test_get_customer_by_id_success(self, client, mock_customer_service):
        mock_customer_data = {
            "id": MOCK_CUSTOMER_ID,
            "name": MOCK_CUSTOMER.name,
            "email": MOCK_CUSTOMER.email
        }
        mock_customer = CustomerFiltered(**mock_customer_data)
        mock_customer_service.get_by_id = AsyncMock(return_value=mock_customer)

        response = client.get(
            f"/api/customer/{MOCK_CUSTOMER_ID}",
            headers={"Authorization": MOCK_TOKEN}
        )

        assert response.status_code == HTTPStatus.OK
        mock_customer_service.get_by_id.assert_called_once_with(MOCK_CUSTOMER_ID)

    @pytest.mark.asyncio
    async def test_create_customer_success(self, client, mock_customer_service):
        # Arrange
        request_data = {
            "name": MOCK_CUSTOMER.name,
            "email": MOCK_CUSTOMER.email
        }
        
        response_data = {
            "id": MOCK_CUSTOMER_ID,
            **request_data
        }

        mock_response = MagicMock(spec=JSONResponse)
        mock_response.status_code = HTTPStatus.CREATED
        mock_response.body = json.dumps(response_data).encode("utf-8")
        

        mock_request = Mock()
        mock_request.json.return_value = request_data
        mock_request.state = Mock(user=Mock(profile="admin"))
        

        with patch("modules.customer.application.service.customer_service.CustomerService.store") as mock_store:
            mock_store.return_value = mock_response
            response = await create_customer(
                request=mock_request,
                customer_service=mock_customer_service,
                customer=MOCK_CUSTOMER
            )

        print(mock_response.status_code)
        print(response)
        print(response.status_code)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == response_data
        mock_customer_service.store.assert_called_once_with(ANY)

    def test_create_customer_forbidden(self, client, mock_customer_service):
        # Arrange
        client.app.state.user = Mock(profile="user")

        # Act
        response = client.post(
            "/api/customer",
            headers={"Authorization": MOCK_TOKEN},
            json=MOCK_CUSTOMER.dict()
        )

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN
        mock_customer_service.store.assert_not_called()

    def test_update_customer_success(self, client, mock_customer_service):
        # Arrange
        mock_customer_service.update = AsyncMock(return_value=MOCK_CUSTOMER)
        client.app.state.user = Mock(profile="admin")

        # Act
        response = client.put(
            f"/api/customer/{MOCK_CUSTOMER_ID}",
            headers={"Authorization": MOCK_TOKEN},
            json=MOCK_CUSTOMER_UPDATE.dict()
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        mock_customer_service.update.assert_called_once_with(
            MOCK_CUSTOMER_ID,
            MOCK_CUSTOMER_UPDATE
        )

    def test_update_customer_forbidden(self, client, mock_customer_service):
        # Arrange
        client.app.state.user = Mock(profile="user")

        # Act
        response = client.put(
            f"/api/customer/{MOCK_CUSTOMER_ID}",
            headers={"Authorization": MOCK_TOKEN},
            json=MOCK_CUSTOMER_UPDATE.dict()
        )

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN
        mock_customer_service.update.assert_not_called()

    def test_delete_customer_success(self, client, mock_customer_service):
        # Arrange
        mock_customer_service.delete = AsyncMock()
        client.app.state.user = Mock(profile="admin")

        # Act
        response = client.delete(
            f"/api/customer/{MOCK_CUSTOMER_ID}",
            headers={"Authorization": MOCK_TOKEN}
        )

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_customer_service.delete.assert_called_once_with(MOCK_CUSTOMER_ID)

    def test_delete_customer_forbidden(self, client, mock_customer_service):
        # Arrange
        client.app.state.user = Mock(profile="user")

        # Act
        response = client.delete(
            f"/api/customer/{MOCK_CUSTOMER_ID}",
            headers={"Authorization": MOCK_TOKEN}
        )

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN
        mock_customer_service.delete.assert_not_called()
