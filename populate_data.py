import random
from datetime import datetime
from elasticsearch import Elasticsearch
from neo4j import GraphDatabase
import os

# Initialize Elasticsearch and Neo4j clients
es = Elasticsearch("http://localhost:9200")
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687")

# Sample data
domains = ["Finance", "Marketing", "Sales", "HR", "Operations"]
categories = ["KPI", "Metric", "Dimension", "Fact", "Attribute"]
statuses = ["Active", "Draft", "Deprecated"]
owners = ["Alice", "Bob", "Charlie", "David", "Eve"]

def create_data_product(id):
    return {
        "id": f"DP{id:03d}",
        "name": f"Data Product {id}",
        "description": f"This is a sample data product {id}",
        "owner": random.choice(owners),
        "input_ports": [
            {
                "name": "Input Port 1",
                "attributes": [
                    {
                        "name": f"Attribute {i}",
                        "data_type": random.choice(["string", "integer", "float", "date"]),
                        "description": f"Description for Attribute {i}",
                        "glossary_term": f"GT{random.randint(1, 50):03d}"
                    } for i in range(1, 4)
                ]
            }
        ],
        "output_ports": [
            {
                "name": "Output Port 1",
                "attributes": [
                    {
                        "name": f"Attribute {i}",
                        "data_type": random.choice(["string", "integer", "float", "date"]),
                        "description": f"Description for Attribute {i}",
                        "glossary_term": f"GT{random.randint(1, 50):03d}"
                    } for i in range(1, 4)
                ]
            }
        ],
        "lineage": {
            "upstream_sources": [f"DP{random.randint(1, 100):03d}" for _ in range(random.randint(0, 3))],
            "downstream_targets": [f"DP{random.randint(1, 100):03d}" for _ in range(random.randint(0, 3))]
        }
    }

def create_glossary_term(id):
    return {
        "term": f"Glossary Term {id}",
        "definition": f"This is the definition for glossary term {id}",
        "domain": random.choice(domains),
        "category": random.choice(categories),
        "owner": random.choice(owners),
        "steward": random.choice(owners),
        "status": random.choice(statuses),
        "created_date": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "version": 1,
        "attributes": {"key": "value"},
        "relationships": [{"related_term": f"GT{random.randint(1, 50):03d}", "relationship_type": "related_to"}],
        "usage_examples": [f"Example {i}" for i in range(1, 4)],
        "notes": "Additional notes"
    }

def populate_elasticsearch():
    for i in range(1, 101):
        dp = create_data_product(i)
        es.index(index="data_products", id=dp["id"], document=dp)

    for i in range(1, 51):
        gt = create_glossary_term(i)
        es.index(index="glossary_terms", id=f"GT{i:03d}", document=gt)

def populate_neo4j():
    with neo4j_driver.session() as session:
        for i in range(1, 101):
            dp = create_data_product(i)
            session.run("""
                CREATE (dp:DataProduct {id: $id, name: $name, owner: $owner})
                WITH dp
                UNWIND $upstream_sources as upstream
                MERGE (us:DataProduct {id: upstream})
                CREATE (us)-[:UPSTREAM]->(dp)
                WITH dp
                UNWIND $downstream_targets as downstream
                MERGE (dt:DataProduct {id: downstream})
                CREATE (dp)-[:DOWNSTREAM]->(dt)
            """, {
                "id": dp["id"],
                "name": dp["name"],
                "owner": dp["owner"],
                "upstream_sources": dp["lineage"]["upstream_sources"],
                "downstream_targets": dp["lineage"]["downstream_targets"]
            })

        for i in range(1, 51):
            gt = create_glossary_term(i)
            session.run("""
                CREATE (gt:GlossaryTerm {id: $id, term: $term, domain: $domain, category: $category})
                WITH gt
                UNWIND $relationships as rel
                MERGE (related:GlossaryTerm {id: rel.related_term})
                CREATE (gt)-[:RELATED_TO]->(related)
            """, {
                "id": f"GT{i:03d}",
                "term": gt["term"],
                "domain": gt["domain"],
                "category": gt["category"],
                "relationships": gt["relationships"]
            })

if __name__ == "__main__":
    print("Populating Elasticsearch...")
    populate_elasticsearch()
    print("Populating Neo4j...")
    populate_neo4j()
    print("Test data population complete!")
