import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService

client = TestClient(app)

@pytest.fixture
def mock_es_service():
    return MagicMock(spec=ElasticsearchService)

@pytest.fixture
def mock_neo4j_service():
    return MagicMock(spec=Neo4jService)

def test_create_data_product(mock_es_service, mock_neo4j_service):
    mock_es_service.index_document.return_value = {"_id": "es_123"}
    mock_neo4j_service.run_query.return_value = [{"id": "neo4j_123"}]

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service
    app.dependency_overrides[Neo4jService] = lambda: mock_neo4j_service

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
        ],
        "lineage": {
            "upstream_sources": ["source1", "source2"],
            "downstream_targets": ["target1", "target2"]
        }
    }

    response = client.post("/api/v1/data-products", json=test_data_product)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Data Product created",
        "elasticsearch_id": "es_123",
        "neo4j_result": [{"id": "neo4j_123"}]
    }

    mock_es_service.index_document.assert_called_once_with("data_products", test_data_product)
    mock_neo4j_service.run_query.assert_called_once()

    app.dependency_overrides.clear()

def test_get_data_product_found(mock_es_service):
    mock_es_service.search.return_value = {
        "hits": {
            "total": {"value": 1},
            "hits": [{"_source": {"id": "dp_123", "name": "Test Data Product", "owner": "test_user"}}]
        }
    }

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service

    response = client.get("/api/v1/data-products/dp_123")

    assert response.status_code == 200
    assert response.json() == {"id": "dp_123", "name": "Test Data Product", "owner": "test_user"}

    mock_es_service.search.assert_called_once_with("data_products", {"query": {"match": {"id": "dp_123"}}})

    app.dependency_overrides.clear()

def test_get_data_product_not_found(mock_es_service):
    mock_es_service.search.return_value = {
        "hits": {
            "total": {"value": 0},
            "hits": []
        }
    }

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service

    response = client.get("/api/v1/data-products/non_existent")

    assert response.status_code == 404
    assert response.json() == {"detail": "Data Product not found"}

    mock_es_service.search.assert_called_once_with("data_products", {"query": {"match": {"id": "non_existent"}}})

    app.dependency_overrides.clear()

def test_get_data_product_lineage(mock_neo4j_service):
    mock_neo4j_service.run_query.return_value = [{
        "id": "dp_123",
        "name": "Test Data Product",
        "upstream_sources": ["source1", "source2"],
        "downstream_targets": ["target1", "target2"]
    }]

    app.dependency_overrides[Neo4jService] = lambda: mock_neo4j_service

    response = client.get("/api/v1/data-products/dp_123/lineage")

    assert response.status_code == 200
    assert response.json() == {
        "id": "dp_123",
        "name": "Test Data Product",
        "upstream_sources": ["source1", "source2"],
        "downstream_targets": ["target1", "target2"]
    }

    mock_neo4j_service.run_query.assert_called_once()

    app.dependency_overrides.clear()

def test_get_data_product_lineage_not_found(mock_neo4j_service):
    mock_neo4j_service.run_query.return_value = []

    app.dependency_overrides[Neo4jService] = lambda: mock_neo4j_service

    response = client.get("/api/v1/data-products/non_existent/lineage")

    assert response.status_code == 404
    assert response.json() == {"detail": "Data Product not found"}

    mock_neo4j_service.run_query.assert_called_once()

    app.dependency_overrides.clear()