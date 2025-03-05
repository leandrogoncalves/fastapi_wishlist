from http import HTTPStatus
import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from modules.wishlist.application.service.wishlist_service import WishlistService
from modules.wishlist.domain.entity.wishlist_product_list import WishlistProductList
from modules.wishlist.infrastructure.http.controller.wishlist_controller import router

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
def client(app, mock_wishlist_service):
    app.dependency_overrides[WishlistService] = lambda: mock_wishlist_service
    return TestClient(app)


@pytest.fixture
def mock_wishlist_service():
    return Mock(spec=WishlistService)

@pytest.fixture
def mock_wishlist_products():
    return WishlistProductList(products=["123", "456"])

@pytest.fixture
def mock_admin_user():
    return {"profile": "admin", "id": "1", "email": "admin@test.com"}

@pytest.fixture
def mock_regular_user():
    return {"profile": "customer", "id": "2", "email": "user@test.com"}

class TestWishlistController:

    @pytest.mark.asyncio
    async def test_get_wishlist_by_customer_success(self, client: TestClient, mock_wishlist_service):
        pytest.skip("Teste incompleto: pendente de conclusão")
        client.app = Mock(state=Mock(user=Mock(profile="admin")))
        customer_id = "customer123"
        expected_response = {
            "products": [
                {"id": "123", "title": "Product 1"},
                {"id": "456", "title": "Product 2"}
            ]
        }
        mock_wishlist_service.get_by_customer_id.return_value = expected_response

        response = client.get(
            f"/api/customer/{customer_id}/wishlist",
            headers={"Authorization": "Bearer valid_token"}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_set_wishlist_admin_success(
        self,
        client: TestClient,
        mock_wishlist_service,
        mock_wishlist_products,
    ):
        pytest.skip("Teste incompleto: pendente de conclusão")
        client.app = Mock(state=Mock(user=Mock(profile="admin")))
        customer_id = "customer123"

        response = client.post(
            f"/api/customer/{customer_id}/wishlist",
            headers={"Authorization": "Bearer valid_token"},
            json={"products": mock_wishlist_products.products}
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_wishlist_service.set_by_customer_id.assert_called_once_with(
            customer_id,
            mock_wishlist_products
        )

    @pytest.mark.asyncio
    async def test_set_wishlist_forbidden_for_regular_user(
        self,
        client: TestClient,
        mock_wishlist_products
    ):
        pytest.skip("Teste incompleto: pendente de conclusão")
        client.app = Mock(state=Mock(user=Mock(profile="viewer")))
        customer_id = "customer123"

        response = client.post(
            f"/api/customer/{customer_id}/wishlist",
            headers={"Authorization": "Bearer valid_token"},
            json={"products": mock_wishlist_products.products}
        )

        assert response.status_code == HTTPStatus.FORBIDDEN

    @pytest.mark.asyncio
    async def test_remove_from_wishlist_admin_success(
        self,
        client: TestClient,
        mock_wishlist_service,
        mock_wishlist_products,
    ):
        pytest.skip("Teste incompleto: pendente de conclusão")
        client.app = Mock(state=Mock(user=Mock(profile="admin")))
        customer_id = "customer123"

        response = client.delete(
            f"/api/customer/{customer_id}/wishlist",
            headers={"Authorization": "Bearer valid_token"},
            json={"products": mock_wishlist_products.products}
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_wishlist_service.remove_by_customer_id.assert_called_once_with(
            customer_id,
            mock_wishlist_products
        )

    @pytest.mark.asyncio
    async def test_remove_from_wishlist_forbidden_for_regular_user(
        self,
        client: TestClient,
        mock_wishlist_products
    ):
        pytest.skip("Teste incompleto: pendente de conclusão")
        client.app = Mock(state=Mock(user=Mock(profile="admin")))
        customer_id = "customer123"

        response = client.delete(
            f"/api/customer/{customer_id}/wishlist",
            headers={"Authorization": "Bearer valid_token"},
            json={"products": mock_wishlist_products.products}
        )

        assert response.status_code == HTTPStatus.FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_wishlist_not_found(self, client: TestClient, mock_wishlist_service):
        pytest.skip("Teste incompleto: pendente de conclusão")
        client.app.state = Mock(user=Mock(profile="admin"))
        customer_id = "nonexistent123"
        mock_wishlist_service.get_by_customer_id.side_effect = HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Wishlist not found"
        )

        response = client.get(
            f"/api/customer/{customer_id}/wishlist",
            headers={"Authorization": "Bearer valid_token"}
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"error": "Wishlist not found"}
