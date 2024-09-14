import os
from elasticsearch import Elasticsearch

class ElasticsearchService:
    def __init__(self):
        elasticsearch_url = os.getenv('ELASTICSEARCH_URL')
        if not elasticsearch_url:
            raise ValueError("ELASTICSEARCH_URL environment variable is not set")
        self.es = Elasticsearch(elasticsearch_url)

    def index_document(self, index, document):
        return self.es.index(index=index, document=document)

    def search(self, index, query, from_: int = 0, size: int = 20):
        return self.es.search(index=index, query=query, from_=from_, size=size)