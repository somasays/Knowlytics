from fastapi import APIRouter, Depends, HTTPException
from app.schemas.data_product import DataProduct
from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService

router = APIRouter()

@router.post("/data-products")
async def create_data_product(data_product: DataProduct, 
                              es_service: ElasticsearchService = Depends(ElasticsearchService),
                              neo4j_service: Neo4jService = Depends(Neo4jService)):
    # Index in Elasticsearch
    es_result = es_service.index_document("data_products", data_product.model_dump())
    
    # Create node in Neo4j
    neo4j_query = (
        "CREATE (dp:DataProduct {id: $id, name: $name, owner: $owner}) "
        "RETURN dp"
    )
    neo4j_result = neo4j_service.run_query(neo4j_query, data_product.dict())
    
    return {"message": "Data Product created", "elasticsearch_id": es_result["_id"], "neo4j_result": neo4j_result}

@router.get("/data-products/{data_product_id}")
async def get_data_product(data_product_id: str, es_service: ElasticsearchService = Depends(ElasticsearchService)):
    result = es_service.search("data_products", {"id": data_product_id})
    hits = result.get("hits", {}).get("hits", [])
    if not hits:
        return {"message": "Data Product not found"}
    return hits[0]["_source"]

@router.get("/test")
async def test_route():
    return {"message": "Test route works"}