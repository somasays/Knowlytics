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

@router.get("/search", response_model=Dict[str, Any])
async def semantic_search(
    query: Optional[str] = Query(None, max_length=100),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search_service: SemanticSearchService = Depends(get_search_service)
):
    from_ = (page - 1) * size
    if not query or not query.strip():
        results = search_service.get_all_results(from_=from_, size=size)  # Update this method
    else:
        results = search_service.search(query, from_=from_, size=size)
    logger.info(f"Search results for query '{query}' - Page {page}: {results}")
    return {"results": results, "page": page, "size": size}