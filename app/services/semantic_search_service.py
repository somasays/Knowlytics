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
            # Perform Elasticsearch search
            es_results = self.es_service.search(
                index="data_products,glossary_terms",
                query={
                    "multi_match": {
                        "query": query,
                        "fields": ["name^2", "description", "term^2", "definition"]
                    }
                }
            )

            combined_results = []
            for hit in es_results["hits"]["hits"]:
                result = {
                    "id": hit["_id"],
                    "type": hit["_index"],
                    "score": hit["_score"],
                    "source": hit["_source"]
                }

                # Get related entities from Neo4j
                related_entities = self.neo4j_service.get_related_entities(hit["_id"])
                result["related_entities"] = related_entities

                # Adjust score based on related entities
                result["score"] += len(related_entities) * 0.1

                combined_results.append(result)

            # Sort by adjusted score
            combined_results.sort(key=lambda x: x["score"], reverse=True)

            return combined_results
        except Exception as e:
            logger.error(f"Error in SemanticSearchService.search: {str(e)}")
            return []  # Return an empty list instead of raising an exception

    def get_all_results(self):
        try:
            es_results = self.es_service.search(
                index="data_products,glossary_terms",
                query={"match_all": {}}
            )

            combined_results = []
            for hit in es_results["hits"]["hits"]:
                result = {
                    "id": hit["_id"],
                    "type": hit["_index"],
                    "score": hit["_score"],
                    "source": hit["_source"]
                }

                related_entities = self.neo4j_service.get_related_entities(hit["_id"])
                result["related_entities"] = related_entities

                result["score"] += len(related_entities) * 0.1

                combined_results.append(result)

            combined_results.sort(key=lambda x: x["score"], reverse=True)

            return combined_results
        except Exception as e:
            logger.error(f"Error in SemanticSearchService.get_all_results: {str(e)}")
            return []