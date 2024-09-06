from neo4j import GraphDatabase
import os

class Neo4jService:
    def __init__(self):
        neo4j_url = os.getenv("NEO4J_URL")
        if not neo4j_url:
            raise ValueError("NEO4J_URL environment variable is not set")
        self.driver = GraphDatabase.driver(neo4j_url)
        
    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def get_related_entities(self, entity_id):
        query = """
        MATCH (n {id: $id})-[r]-(related)
        RETURN type(r) as relationship_type, related.id as related_id, labels(related) as related_labels
        """
        return self.run_query(query, {"id": entity_id})