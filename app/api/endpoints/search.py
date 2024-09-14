from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Dict, Any
from app.services.semantic_search_service import SemanticSearchService
from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_search_service(
    es_service: ElasticsearchService = Depends(),
    neo4j_service: Neo4jService = Depends()
) -> SemanticSearchService:
    return SemanticSearchService(es_service, neo4j_service)

@router.get("/search", response_model=Dict[str, List[Dict[str, Any]]])
async def semantic_search(
    query: Optional[str] = Query(None, max_length=100),
    search_service: SemanticSearchService = Depends(get_search_service)
):
    if not query or not query.strip():
        results = search_service.get_all_results()  # Implement this method
    else:
        results = search_service.search(query)
    logger.info(f"Search results for query '{query}': {results}")
    return {"results": results}