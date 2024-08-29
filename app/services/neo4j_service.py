from neo4j import GraphDatabase
import os

class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(os.getenv("NEO4J_URL"))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]