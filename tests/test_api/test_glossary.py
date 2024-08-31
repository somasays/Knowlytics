import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, ANY
from datetime import datetime, timedelta

from app.main import app
from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService
from app.schemas.glossary_term import GlossaryTerm

client = TestClient(app)

@pytest.fixture
def mock_es_service(mocker):
    return mocker.Mock(spec=ElasticsearchService)

@pytest.fixture
def mock_neo4j_service(mocker):
    return mocker.Mock(spec=Neo4jService)

def test_create_glossary_term():
    mock_es_service = MagicMock(spec=ElasticsearchService)
    mock_neo4j_service = MagicMock(spec=Neo4jService)

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

    # Get the actual call arguments
    actual_call = mock_es_service.index_document.call_args

    # Assert that the index name is correct
    assert actual_call[0][0] == "glossary_terms"

    # Assert that all the fields in test_glossary_term are present in the actual call
    for key, value in test_glossary_term.items():
        assert actual_call[0][1][key] == value

    # Assert that created_date and last_updated are present and are recent timestamps
    now = datetime.now()
    for date_field in ['created_date', 'last_updated']:
        assert date_field in actual_call[0][1]
        actual_date = datetime.fromisoformat(actual_call[0][1][date_field])
        assert now - timedelta(minutes=1) <= actual_date <= now

    # Assert that other fields are present with None values
    for field in ['steward', 'attributes', 'relationships', 'usage_examples', 'notes']:
        assert actual_call[0][1].get(field) is None

    # ... (keep the rest of the test code)

def test_get_glossary_term_found():
    mock_es_service = MagicMock(spec=ElasticsearchService)
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

    try:
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
    finally:
        app.dependency_overrides.clear()

def test_get_glossary_term_not_found():
    mock_es_service = MagicMock(spec=ElasticsearchService)
    mock_es_service.search.return_value = {
        "hits": {
            "total": {"value": 0},
            "hits": []
        }
    }

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service

    try:
        response = client.get("/api/v1/glossary-terms/Non%20Existent%20Term")

        assert response.status_code == 200
        assert response.json() == {"message": "Glossary Term not found"}

        mock_es_service.search.assert_called_once_with("glossary_terms", {"query": {"match": {"term": "Non Existent Term"}}})
    finally:
        app.dependency_overrides.clear()

def test_create_glossary_term_with_optional_fields():
    mock_es_service = MagicMock(spec=ElasticsearchService)
    mock_neo4j_service = MagicMock(spec=Neo4jService)

    mock_es_service.index_document.return_value = {"_id": "es_124"}
    mock_neo4j_service.run_query.return_value = [{"gt": {"id": "neo4j_124"}}]

    app.dependency_overrides[ElasticsearchService] = lambda: mock_es_service
    app.dependency_overrides[Neo4jService] = lambda: mock_neo4j_service

    try:
        test_glossary_term = {
            "term": "Advanced Term",
            "definition": "This is an advanced test term",
            "domain": "Advanced Domain",
            "category": "Advanced Category",
            "owner": "advanced_user",
            "steward": "steward_user",
            "status": "Draft",
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
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

        mock_es_service.index_document.assert_called_once_with("glossary_terms", test_glossary_term)
        mock_neo4j_service.run_query.assert_called_once()
    finally:
        app.dependency_overrides.clear()
