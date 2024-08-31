from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService

class SemanticSearchService:
    def __init__(self, es_service: ElasticsearchService, neo4j_service: Neo4jService):
        self.es_service = es_service
        self.neo4j_service = neo4j_service

    def search(self, query: str):
        # Perform Elasticsearch full-text search
        es_results = self.es_service.search("data_products,glossary_terms", {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["name", "description", "term", "definition"]
                }
            }
        })

        # Extract IDs from Elasticsearch results
        ids = [hit["_id"] for hit in es_results["hits"]["hits"]]

        # Perform Neo4j graph search for related entities
        neo4j_query = (
            "MATCH (n) WHERE n.id IN $ids OR n.term IN $ids "
            "WITH n "
            "OPTIONAL MATCH (n)-[r]-(related) "
            "RETURN n, type(r) as relationship_type, related"
        )
        graph_results = self.neo4j_service.run_query(neo4j_query, {"ids": ids})

        # Combine and rank results (basic ranking for now)
        combined_results = []
        for hit in es_results["hits"]["hits"]:
            result = hit["_source"]
            result["score"] = hit["_score"]
            result["related_entities"] = [
                item["related"] for item in graph_results 
                if item["n"]["id"] == hit["_id"] or item["n"]["term"] == hit["_id"]
            ]
            combined_results.append(result)

        # Sort by Elasticsearch score (basic ranking)
        combined_results.sort(key=lambda x: x["score"], reverse=True)

        return combined_results