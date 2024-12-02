import os
from elasticsearch import Elasticsearch

es_url = os.environ.get("ES_URL")
es_key = os.environ.get("ES_TOKEN")


def create_ind(index_name):
    client = Elasticsearch(es_url, api_key=es_key)
    client.indices.create(index=index_name)