from fastapi import FastAPI
from elasticsearch import Elasticsearch
from neo4j import GraphDatabase
import os
from app.api.endpoints import data_products, glossary, search

app = FastAPI()
app.include_router(data_products.router, prefix="/api/v1")
app.include_router(glossary.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    es_client = Elasticsearch(os.getenv("ELASTICSEARCH_URL"))
    neo4j_driver = GraphDatabase.driver(os.getenv("NEO4J_URL"))

    es_health = "Healthy" if es_client.ping() else "Unhealthy"

    neo4j_health = "Healthy"
    try:
        with neo4j_driver.session() as session:
            session.run("RETURN 1")
    except Exception:
        neo4j_health = "Unhealthy"

    return {
        "elasticsearch": es_health,
        "neo4j": neo4j_health
    }