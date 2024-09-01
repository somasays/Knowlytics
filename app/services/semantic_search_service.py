from app.services.elasticsearch_service import ElasticsearchService
from app.services.neo4j_service import Neo4jService

import logging

logger = logging.getLogger(__name__)

class SemanticSearchService:
    def __init__(self, es_service: ElasticsearchService, neo4j_service: Neo4jService):
        self.es_service = es_service
        self.neo4j_service = neo4j_service

    def search(self, query: str):
        try:
            # Perform Elasticsearch full-text search
            es_results = self.es_service.search("data_products,glossary_terms", {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name", "description", "term", "definition"]
                    }
                }
            })

            combined_results = []
            for hit in es_results['hits']['hits']:
                result = {
                    "id": hit["_id"],
                    "name": hit["_source"].get("name") or hit["_source"].get("term"),
                    "description": hit["_source"].get("description") or hit["_source"].get("definition"),
                    "type": "data_product" if "name" in hit["_source"] else "glossary_term",
                    "score": hit["_score"],
                    "related_entities": []
                }

                # Get related entities from Neo4j
                related = self.neo4j_service.get_related_entities(result["id"])
                for item in related:
                    result["related_entities"].append({
                        "entity": item["related"],
                        "relationship_type": item["relationship_type"]
                    })
                    connection_count = item["connection_count"]
                
                # Adjust score based on connection count
                result["score"] *= (1 + (connection_count * 0.1))
                combined_results.append(result)

            # Sort by adjusted score
            combined_results.sort(key=lambda x: x["score"], reverse=True)

            return combined_results
        except Exception as e:
            logger.error(f"Error in SemanticSearchService.search: {str(e)}")
            return []  # Return an empty list instead of raising an exception