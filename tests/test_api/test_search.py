from fastapi import Depends
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from app.main import app
from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService
from app.services.semantic_search_service import SemanticSearchService
from app.api.endpoints.search import get_search_service  # Add this import

client = TestClient(app)

@pytest.fixture
def mock_es_service():
    return MagicMock(spec=ElasticsearchService)

@pytest.fixture
def mock_neo4j_service():
    return MagicMock(spec=Neo4jService)

@pytest.fixture
def mock_semantic_search_service(mock_es_service, mock_neo4j_service):
    mock = MagicMock(spec=SemanticSearchService)
    mock.es_service = mock_es_service
    mock.neo4j_service = mock_neo4j_service
    return mock

def get_mock_search_service(mock_semantic_search_service):
    def _get_mock_search_service():
        return mock_semantic_search_service
    return _get_mock_search_service

@patch.object(ElasticsearchService, '__init__', return_value=None)
@patch.object(Neo4jService, '__init__', return_value=None)
def test_successful_search_with_results(mock_neo4j_init, mock_es_init, mock_es_service, mock_neo4j_service, mock_semantic_search_service):
    mock_results = [
        {
            "id": "DP001",
            "name": "Customer Data",
            "description": "Detailed customer information",
            "score": 0.95,
            "related_entities": []
        }
    ]
    mock_semantic_search_service.search.return_value = mock_results

    app.dependency_overrides[get_search_service] = get_mock_search_service(mock_semantic_search_service)

    try:
        response = client.get("/api/v1/search", params={"query": "customer"})

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.json()}")
        print(f"Mock called: {mock_semantic_search_service.search.called}")
        print(f"Mock call args: {mock_semantic_search_service.search.call_args}")

        assert response.status_code == 200
        assert response.json() == {"results": mock_results}
        mock_semantic_search_service.search.assert_called_once_with("customer")
    finally:
        app.dependency_overrides.clear()

@patch.object(ElasticsearchService, '__init__', return_value=None)
@patch.object(Neo4jService, '__init__', return_value=None)
def test_empty_query(mock_neo4j_init, mock_es_init, mock_semantic_search_service):
    app.dependency_overrides[get_search_service] = get_mock_search_service(mock_semantic_search_service)

    try:
        response = client.get("/api/v1/search", params={"query": ""})
        assert response.status_code == 422
        assert "detail" in response.json()
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == "string_too_short"
        assert error_detail["loc"] == ["query", "query"]
        assert "String should have at least 1 characters" in error_detail["msg"]
    finally:
        app.dependency_overrides.clear()

@patch.object(ElasticsearchService, '__init__', return_value=None)
@patch.object(Neo4jService, '__init__', return_value=None)
def test_search_with_no_results(mock_neo4j_init, mock_es_init, mock_semantic_search_service):
    mock_semantic_search_service.search.return_value = []

    app.dependency_overrides[get_search_service] = lambda: mock_semantic_search_service

    try:
        response = client.get("/api/v1/search?query=nonexistent")
        
        assert response.status_code == 200
        assert response.json() == {"results": []}
        mock_semantic_search_service.search.assert_called_once_with("nonexistent")
    finally:
        app.dependency_overrides.clear()

@patch.object(ElasticsearchService, '__init__', return_value=None)
@patch.object(Neo4jService, '__init__', return_value=None)
def test_error_handling(mock_neo4j_init, mock_es_init, mock_semantic_search_service):
    mock_semantic_search_service.search.side_effect = Exception("Internal server error")

    app.dependency_overrides[get_search_service] = lambda: mock_semantic_search_service

    try:
        response = client.get("/api/v1/search?query=error")
        
        assert response.status_code == 500
        assert response.json() == {"detail": "An error occurred during the search: Internal server error"}
        mock_semantic_search_service.search.assert_called_once_with("error")
    finally:
        app.dependency_overrides.clear()

@patch.object(ElasticsearchService, '__init__', return_value=None)
@patch.object(Neo4jService, '__init__', return_value=None)
def test_search_with_related_entities(mock_es_service, mock_neo4j_service, mock_semantic_search_service):
    mock_results = [
        {
            "id": "DP001",
            "name": "Customer Data",
            "description": "Detailed customer information",
            "score": 0.95,
            "related_entities": [
                {"id": "DP002", "name": "Order History"},
                {"id": "DP003", "name": "Customer Preferences"}
            ]
        }
    ]
    mock_semantic_search_service.search.return_value = mock_results

    app.dependency_overrides[get_search_service] = lambda: mock_semantic_search_service

    try:
        response = client.get("/api/v1/search?query=customer")
        
        assert response.status_code == 200
        assert response.json() == {"results": mock_results}
        assert len(response.json()["results"][0]["related_entities"]) == 2
        mock_semantic_search_service.search.assert_called_once_with("customer")
    finally:
        app.dependency_overrides.clear()

@patch.object(ElasticsearchService, '__init__', return_value=None)
@patch.object(Neo4jService, '__init__', return_value=None)
def test_multiple_search_results(mock_neo4j_init, mock_es_init, mock_semantic_search_service):
    mock_results = [
        {
            "id": "DP001",
            "name": "Customer Data",
            "description": "Detailed customer information",
            "score": 0.95,
            "related_entities": []
        },
        {
            "id": "DP002",
            "name": "Order History",
            "description": "Customer order records",
            "score": 0.85,
            "related_entities": []
        },
        {
            "id": "DP003",
            "name": "Customer Preferences",
            "description": "Customer likes and dislikes",
            "score": 0.75,
            "related_entities": []
        }
    ]
    mock_semantic_search_service.search.return_value = mock_results

    app.dependency_overrides[get_search_service] = lambda: mock_semantic_search_service

    try:
        response = client.get("/api/v1/search?query=customer")
        
        assert response.status_code == 200
        assert response.json() == {"results": mock_results}
        assert len(response.json()["results"]) == 3
        mock_semantic_search_service.search.assert_called_once_with("customer")
    finally:
        app.dependency_overrides.clear()
