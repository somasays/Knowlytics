from elasticsearch import Elasticsearch
import os

class ElasticsearchService:
    def __init__(self):
        self.es = Elasticsearch(os.getenv("ELASTICSEARCH_URL"))

    def index_document(self, index, document):
        return self.es.index(index=index, document=document)

    def search(self, index, query):
        return self.es.search(index=index, query=query)