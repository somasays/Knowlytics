from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.semantic_search_service import SemanticSearchService
from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService
from typing import List, Dict, Any

router = APIRouter()

def get_search_service(
    es_service: ElasticsearchService = Depends(),
    neo4j_service: Neo4jService = Depends()
) -> SemanticSearchService:
    return SemanticSearchService(es_service, neo4j_service)

@router.get("/search", response_model=Dict[str, List[Dict[str, Any]]])
async def semantic_search(
    query: str = Query(..., min_length=1, max_length=100),
    search_service: SemanticSearchService = Depends(get_search_service)
):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    try:
        results = search_service.search(query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during the search: {str(e)}")