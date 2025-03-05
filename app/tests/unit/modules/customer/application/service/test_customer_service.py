import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from http import HTTPStatus
from fastapi import HTTPException
from modules.customer.application.service.customer_service import CustomerService
from modules.customer.domain.entity.customer import Customer, CustomerUp
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from modules.core.config.env import PAGE_SIZE, DEFAULT_TINE_ZONE

# Test data
MOCK_CUSTOMER_ID = "123-abc"
MOCK_EMAIL = "test@teste.com"
MOCK_CUSTOMER = Customer(
    name="Test User",
    email=MOCK_EMAIL,
    password="123456",
    profile="viewer"
)

class TestCustomerService:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def service(self, mock_repository):
        service = CustomerService()
        service._get_customer_repository = Mock(return_value=mock_repository)
        return service

    async def test_get_all_paginated_success(self, service, mock_repository):
        pytest.skip("Teste incompleto: pendente de conclusão")
        # Arrange
        page = 1
        mock_customers = [
            CustomerModel(id="1", name="User1", email="user1@test.com"),
            CustomerModel(id="2", name="User2", email="user2@test.com")
        ]
        mock_repository.count = AsyncMock(return_value=2)
        mock_repository.get_all_customers = AsyncMock(return_value=mock_customers)

        # Act
        result = await service.get_all_paginated(page)

        # Assert
        assert result.page == page
        assert result.total_results == 2
        assert result.results_in_page == 2
        mock_repository.get_all_customers.assert_called_once_with((page - 1) * PAGE_SIZE, PAGE_SIZE)

    async def test_get_by_id_success(self, service, mock_repository):
        pytest.skip("Teste incompleto: pendente de conclusão")
        mock_customer = CustomerModel(
            id=MOCK_CUSTOMER_ID,
            name=MOCK_CUSTOMER.name,
            email=MOCK_CUSTOMER.email
        )
        mock_repository.get_by_id = AsyncMock(return_value=mock_customer)

        result = await service.get_by_id(MOCK_CUSTOMER_ID)

        assert result.id == MOCK_CUSTOMER_ID
        assert result.name == MOCK_CUSTOMER.name
        mock_repository.get_by_id.assert_called_once_with(MOCK_CUSTOMER_ID)

    async def test_get_by_id_not_found(self, service, mock_repository):
        pytest.skip("Teste incompleto: pendente de conclusão")
        mock_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc:
            await service.get_by_id(MOCK_CUSTOMER_ID)
        assert exc.value.status_code == HTTPStatus.NOT_FOUND

    async def test_store_success(self, service, mock_repository):
        pytest.skip("Teste incompleto: pendente de conclusão")
        mock_repository.get_by_email = AsyncMock(return_value=None)
        mock_repository.create = AsyncMock(return_value=CustomerModel(
            id=MOCK_CUSTOMER_ID,
            name=MOCK_CUSTOMER.name,
            email=MOCK_CUSTOMER.email
        ))

        result = await service.store(MOCK_CUSTOMER)

        assert result.email == MOCK_CUSTOMER.email
        mock_repository.create.assert_called_once()

    async def test_store_duplicate_email(self, service, mock_repository):
        pytest.skip("Teste incompleto: pendente de conclusão")
        mock_repository.get_by_email = AsyncMock(return_value=CustomerModel())

        with pytest.raises(HTTPException) as exc:
            await service.store(MOCK_CUSTOMER)
        assert exc.value.status_code == HTTPStatus.PRECONDITION_FAILED

    async def test_update_success(self, service, mock_repository):
        pytest.skip("Teste incompleto: pendente de conclusão")
        mock_customer = CustomerModel(
            id=MOCK_CUSTOMER_ID,
            name=MOCK_CUSTOMER.name,
            email=MOCK_CUSTOMER.email
        )
        mock_repository.get_by_id = AsyncMock(return_value=mock_customer)
        mock_repository.get_by_email = AsyncMock(return_value=None)
        mock_repository.update = AsyncMock(return_value=mock_customer)

        update_data = CustomerUp(
            name="Updated Name",
            email="updated@test.com"
        )

        result = await service.update(MOCK_CUSTOMER_ID, update_data)

        assert result.id == MOCK_CUSTOMER_ID
        mock_repository.update.assert_called_once()

    async def test_delete_success(self, service, mock_repository):
        pytest.skip("Teste incompleto: pendente de conclusão")
        mock_customer = CustomerModel(
            id=MOCK_CUSTOMER_ID,
            name=MOCK_CUSTOMER.name,
            email=MOCK_CUSTOMER.email
        )
        mock_repository.get_by_id = AsyncMock(return_value=mock_customer)
        mock_repository.delete = AsyncMock()

        await service.delete(MOCK_CUSTOMER_ID)

        mock_repository.delete.assert_called_once_with(mock_customer)

    async def test_delete_not_found(self, service, mock_repository):
        pytest.skip("Teste incompleto: pendente de conclusão")
        mock_repository.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc:
            await service.delete(MOCK_CUSTOMER_ID)
        assert exc.value.status_code == HTTPStatus.NOT_FOUND
