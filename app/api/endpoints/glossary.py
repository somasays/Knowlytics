from fastapi import APIRouter, Depends
from app.schemas.glossary_term import GlossaryTerm
from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService

router = APIRouter()

@router.post("/glossary-terms")
async def create_glossary_term(glossary_term: GlossaryTerm,
                               es_service: ElasticsearchService = Depends(ElasticsearchService),
                               neo4j_service: Neo4jService = Depends(Neo4jService)):
    # Use the model's dict method to get all fields, including defaults
    glossary_term_dict = glossary_term.model_dump()
    
    # Index in Elasticsearch
    es_result = es_service.index_document("glossary_terms", glossary_term_dict)

    # Create node in Neo4j
    neo4j_query = (
        "CREATE (gt:GlossaryTerm {term: $term, domain: $domain, category: $category}) "
        "RETURN gt"
    )
    neo4j_result = neo4j_service.run_query(neo4j_query, glossary_term_dict)

    return {"message": "Glossary Term created", "elasticsearch_id": es_result["_id"], "neo4j_result": neo4j_result}

@router.get("/glossary-terms/{term}")
async def get_glossary_term(term: str,
                            es_service: ElasticsearchService = Depends(ElasticsearchService)):
    es_result = es_service.search("glossary_terms", {"query": {"match": {"term": term}}})
    if es_result["hits"]["total"]["value"] > 0:
        return es_result["hits"]["hits"][0]["_source"]
    return {"message": "Glossary Term not found"}