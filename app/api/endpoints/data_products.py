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
    
    # Create node and relationships in Neo4j
    neo4j_query = (
        "CREATE (dp:DataProduct {id: $id, name: $name, owner: $owner}) "
        "WITH dp "
        "UNWIND $upstream_sources as upstream "
        "MATCH (us:DataProduct {id: upstream}) "
        "CREATE (us)-[:UPSTREAM]->(dp) "
        "WITH dp "
        "UNWIND $downstream_targets as downstream "
        "MATCH (dt:DataProduct {id: downstream}) "
        "CREATE (dp)-[:DOWNSTREAM]->(dt) "
        "RETURN dp"
    )
    neo4j_params = data_product.model_dump()
    neo4j_params.update({
        "upstream_sources": data_product.lineage.upstream_sources,
        "downstream_targets": data_product.lineage.downstream_targets
    })
    neo4j_result = neo4j_service.run_query(neo4j_query, neo4j_params)
    
    return {"message": "Data Product created", "elasticsearch_id": es_result["_id"], "neo4j_result": neo4j_result}

@router.get("/data-products/{data_product_id}")
async def get_data_product(data_product_id: str,
                           es_service: ElasticsearchService = Depends(ElasticsearchService)):
    es_result = es_service.search("data_products", {"query": {"match": {"id": data_product_id}}})
    if es_result["hits"]["total"]["value"] > 0:
        return es_result["hits"]["hits"][0]["_source"]
    raise HTTPException(status_code=404, detail="Data Product not found")

@router.get("/data-products/{data_product_id}/lineage")
async def get_data_product_lineage(data_product_id: str,
                                   neo4j_service: Neo4jService = Depends(Neo4jService)):
    neo4j_query = (
        "MATCH (dp:DataProduct {id: $id}) "
        "OPTIONAL MATCH (upstream)-[:UPSTREAM]->(dp) "
        "OPTIONAL MATCH (dp)-[:DOWNSTREAM]->(downstream) "
        "RETURN dp.id as id, dp.name as name, "
        "collect(DISTINCT upstream.id) as upstream_sources, "
        "collect(DISTINCT downstream.id) as downstream_targets"
    )
    result = neo4j_service.run_query(neo4j_query, {"id": data_product_id})
    if result:
        return result[0]
    raise HTTPException(status_code=404, detail="Data Product not found")

# Removed test route