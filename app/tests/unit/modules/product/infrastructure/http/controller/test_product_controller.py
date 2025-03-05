from http import HTTPStatus
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from modules.product.domain.entity.product import Product, ProductUp
from modules.product.domain.entity.product_paginated import ProductPaginated
from modules.product.application.service.product_service import ProductService
from modules.product.infrastructure.http.controller.product_controller import router, create_product


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def mock_product_service():
    return Mock(spec=ProductService)


@pytest.fixture
def mock_product():
    return Product(
        id="123",
        title="Test Product",
        price=99.99,
        image="http://test.com/image.jpg",
        brand="Test Brand"
    )


@pytest.fixture
def mock_admin_user():
    return {"profile": "admin", "id": "1", "email": "admin@test.com"}


@pytest.fixture
def mock_regular_user():
    return {"profile": "viewer", "id": "2", "email": "user@test.com"}


@pytest.fixture
def mock_product_service():
    return Mock(spec=ProductService)


@pytest.fixture
def client(app, mock_product_service):
    app.dependency_overrides[ProductService] = lambda: mock_product_service
    return TestClient(app)


class TestProductController:

    @pytest.mark.asyncio
    async def test_get_products_success(
            self,
            client: TestClient,
            mock_product_service,
            mock_product
    ):
        paginated = ProductPaginated(
            page=1,
            total_pages=1,
            total_results=1,
            results_in_page=1,
            data=[mock_product.to_dict()]
        )
        mock_product_service.get_all_paginated.return_value = paginated

        response = client.get(
            "/api/product",
            headers={"Authorization": "Bearer valid_token"}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()["total_results"] == 1
        assert len(response.json()["data"]) == 1

    @pytest.mark.asyncio
    async def test_get_product_by_id_success(
            self,
            client: TestClient,
            mock_product_service,
            mock_product
    ):
        mock_product_service.get_by_id.return_value = mock_product
        print('mock_product')
        print(mock_product)

        response = client.get(
            f"/api/product/{mock_product.id}",
            headers={"Authorization": "Bearer valid_token"}
        )
        print('response.json()')
        print(response.json())

        assert response.status_code == HTTPStatus.OK
        assert response.json()["id"] == mock_product.id

    @pytest.mark.asyncio
    async def test_create_product_admin_success(
            self,
            client: TestClient,
            mock_product_service,
            mock_product):
        pytest.skip("Teste incompleto: pendente de conclusão")
        mock_product_service.store.return_value = mock_product

        response = client.post(
            "/api/product",
            headers={"Authorization": "Bearer valid_token"},
            json=mock_product
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()["id"] == mock_product["id"]

    @pytest.mark.asyncio
    async def test_create_product_forbidden_for_regular_user(
            self,
            client: TestClient,
            mock_product
    ):
        pytest.skip("Teste incompleto: pendente de conclusão")
        response = client.post(
            "/api/product",
            headers={"Authorization": "Bearer valid_token"},
            json=mock_product.to_dict()
        )

        assert response.status_code == HTTPStatus.FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_product_admin_success(
            self,
            client: TestClient,
            mock_product_service,
            mock_product,
    ):
        pytest.skip("Teste incompleto: pendente de conclusão")
        product_up = ProductUp(
            title="Updated Product",
            price=199.99,
            image="http://test.com/updated.jpg",
            brand="Updated Brand"
        )
        mock_product_service.update.return_value = mock_product

        response = client.put(
            f"/api/product/{mock_product.id}",
            headers={"Authorization": "Bearer valid_token"},
            json=product_up.to_dict()
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()["id"] == mock_product.id

    @pytest.mark.asyncio
    async def test_delete_product_admin_success(
            self,
            client: TestClient,
            mock_product):
        pytest.skip("Teste incompleto: pendente de conclusão")
        response = client.delete(
            f"/api/product/{mock_product.id}",
            headers={"Authorization": "Bearer valid_token"}
        )

        assert response.status_code == HTTPStatus.NO_CONTENT

    @pytest.mark.asyncio
    async def test_delete_product_forbidden_for_regular_user(
            self,
            client: TestClient,
            mock_product
    ):
        pytest.skip("Teste incompleto: pendente de conclusão")
        response = client.delete(
            f"/api/product/{mock_product.id}",
            headers={"Authorization": "Bearer valid_token"}
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
