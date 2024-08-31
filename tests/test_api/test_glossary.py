import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime, timedelta

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

def test_create_glossary_term(mock_es_service, mock_neo4j_service):
    mock_es_service.index_document.return_value = {"_id": "es_123"}
    mock_neo4j_service.run_query.return_value = [{"gt": {"id": "neo4j_123"}}]

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service
    app.dependency_overrides[Neo4jService] = lambda: mock_neo4j_service

    test_glossary_term = {
        "term": "Test Term",
        "definition": "This is a test term",
        "domain": "Test Domain",
        "category": "Test Category",
        "owner": "test_user",
        "status": "Active",
        "version": 1
    }

    response = client.post("/api/v1/glossary-terms", json=test_glossary_term)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Glossary Term created",
        "elasticsearch_id": "es_123",
        "neo4j_result": [{"gt": {"id": "neo4j_123"}}]
    }

    actual_call = mock_es_service.index_document.call_args[0][1]
    assert actual_call["term"] == "Test Term"
    assert actual_call["definition"] == "This is a test term"
    assert actual_call["domain"] == "Test Domain"
    assert actual_call["category"] == "Test Category"
    assert actual_call["owner"] == "test_user"
    assert actual_call["status"] == "Active"
    assert actual_call["version"] == 1

    now = datetime.now()
    for date_field in ['created_date', 'last_updated']:
        assert date_field in actual_call
        actual_date = datetime.fromisoformat(actual_call[date_field])
        assert now - timedelta(minutes=1) <= actual_date <= now

    for field in ['steward', 'attributes', 'relationships', 'usage_examples', 'notes']:
        assert actual_call.get(field) is None

    mock_neo4j_service.run_query.assert_called_once()

    app.dependency_overrides.clear()

def test_get_glossary_term_found(mock_es_service):
    mock_es_service.search.return_value = {
        "hits": {
            "total": {"value": 1},
            "hits": [{"_source": {
                "term": "Test Term",
                "definition": "This is a test term",
                "domain": "Test Domain",
                "category": "Test Category",
                "owner": "test_user",
                "status": "Active",
                "created_date": "2023-04-20T10:00:00",
                "last_updated": "2023-04-20T10:00:00",
                "version": 1
            }}]
        }
    }

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service

    response = client.get("/api/v1/glossary-terms/Test%20Term")

    assert response.status_code == 200
    assert response.json() == {
        "term": "Test Term",
        "definition": "This is a test term",
        "domain": "Test Domain",
        "category": "Test Category",
        "owner": "test_user",
        "status": "Active",
        "created_date": "2023-04-20T10:00:00",
        "last_updated": "2023-04-20T10:00:00",
        "version": 1
    }

    mock_es_service.search.assert_called_once_with("glossary_terms", {"query": {"match": {"term": "Test Term"}}})

    app.dependency_overrides.clear()

def test_get_glossary_term_not_found(mock_es_service):
    mock_es_service.search.return_value = {
        "hits": {
            "total": {"value": 0},
            "hits": []
        }
    }

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service

    response = client.get("/api/v1/glossary-terms/Non%20Existent%20Term")

    assert response.status_code == 200
    assert response.json() == {"message": "Glossary Term not found"}

    mock_es_service.search.assert_called_once_with("glossary_terms", {"query": {"match": {"term": "Non Existent Term"}}})

    app.dependency_overrides.clear()

def test_create_glossary_term_with_optional_fields(mock_es_service, mock_neo4j_service):
    mock_es_service.index_document.return_value = {"_id": "es_124"}
    mock_neo4j_service.run_query.return_value = [{"gt": {"id": "neo4j_124"}}]

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service
    app.dependency_overrides[Neo4jService] = lambda: mock_neo4j_service

    test_glossary_term = {
        "term": "Advanced Term",
        "definition": "This is an advanced test term",
        "domain": "Advanced Domain",
        "category": "Advanced Category",
        "owner": "advanced_user",
        "steward": "steward_user",
        "status": "Draft",
        "version": 1,
        "attributes": {"key1": "value1", "key2": "value2"},
        "relationships": [{"related_term": "Related Term 1"}, {"related_term": "Related Term 2"}],
        "usage_examples": ["Example 1", "Example 2"],
        "notes": "Additional notes for the term"
    }

    response = client.post("/api/v1/glossary-terms", json=test_glossary_term)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Glossary Term created",
        "elasticsearch_id": "es_124",
        "neo4j_result": [{"gt": {"id": "neo4j_124"}}]
    }

    actual_call = mock_es_service.index_document.call_args[0][1]
    for key, value in test_glossary_term.items():
        assert actual_call[key] == value

    assert 'created_date' in actual_call
    assert 'last_updated' in actual_call

    mock_neo4j_service.run_query.assert_called_once()

    app.dependency_overrides.clear()
