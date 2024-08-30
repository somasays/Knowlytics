import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from unittest.mock import patch, MagicMock

from app.main import app
from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService
from app.api.endpoints.data_products import get_data_product

client = TestClient(app)

@pytest.fixture
def mock_es_service(mocker):
    mock = mocker.Mock(spec=ElasticsearchService)
    return mock

@pytest.fixture
def mock_neo4j_service(mocker):
    mock = mocker.Mock(spec=Neo4jService)
    return mock

def test_create_data_product():
    # Create mocks for both services
    mock_es_service = MagicMock(spec=ElasticsearchService)
    mock_neo4j_service = MagicMock(spec=Neo4jService)

    # Set up return values for the mocks
    mock_es_service.index_document.return_value = {"_id": "es_123"}
    mock_neo4j_service.run_query.return_value = [{"id": "neo4j_123"}]

    # Use FastAPI's dependency_overrides to inject the mocks
    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service
    app.dependency_overrides[Neo4jService] = lambda: mock_neo4j_service

    try:
        test_data_product = {
            "id": "dp_123",
            "name": "Test Data Product",
            "description": "This is a test data product",
            "owner": "test_user",
            "input_ports": [
                {
                    "name": "Input Port 1",
                    "attributes": [
                        {
                            "name": "attribute1",
                            "data_type": "string",
                            "description": "Test attribute",
                            "glossary_term": "test_term"
                        }
                    ]
                }
            ],
            "output_ports": [
                {
                    "name": "Output Port 1",
                    "attributes": [
                        {
                            "name": "attribute2",
                            "data_type": "integer",
                            "description": "Test output attribute",
                            "glossary_term": None
                        }
                    ]
                }
            ]
        }

        response = client.post("/api/v1/data-products", json=test_data_product)

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        assert response.status_code == 200
        assert response.json() == {
            "message": "Data Product created",
            "elasticsearch_id": "es_123",
            "neo4j_result": [{"id": "neo4j_123"}]
        }

        # Assert that the mocks were called with the expected arguments
        mock_es_service.index_document.assert_called_once_with("data_products", test_data_product)
        mock_neo4j_service.run_query.assert_called_once()
    finally:
        # Clear the dependency overrides after the test
        app.dependency_overrides.clear()

def test_get_data_product_found():
    # Create a mock for ElasticsearchService
    mock_es_service = MagicMock(spec=ElasticsearchService)
    mock_es_service.search.return_value = {
        "hits": {
            "total": {"value": 1},
            "hits": [{"_source": {"id": "dp_123", "name": "Test Data Product", "owner": "test_user"}}]
        }
    }

    # Use FastAPI's dependency_overrides to inject the mock
    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service

    try:
        response = client.get("/api/v1/data-products/dp_123")

        assert response.status_code == 200
        assert response.json() == {"id": "dp_123", "name": "Test Data Product", "owner": "test_user"}

        mock_es_service.search.assert_called_once_with("data_products", {"id": "dp_123"})
    finally:
        # Clear the dependency override after the test
        app.dependency_overrides.clear()

@patch('app.api.endpoints.data_products.ElasticsearchService')
def test_get_data_product_not_found(mock_es_service):
    mock_es_instance = MagicMock()
    mock_es_instance.search.return_value = {
        "hits": {
            "total": {"value": 0},
            "hits": []
        }
    }
    mock_es_service.return_value = mock_es_instance

    # Override the dependency
    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_instance

    try:
        response = client.get("/api/v1/data-products/non_existent")

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        assert response.status_code == 200
        assert response.json() == {"message": "Data Product not found"}

        mock_es_instance.search.assert_called_once_with("data_products", {"id": "non_existent"})
    finally:
        # Clean up the override after the test
        app.dependency_overrides.clear()

def test_test_route():
    response = client.get("/api/v1/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Test route works"}