from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


def get_elasticsearch_client():
    try:
        es = Elasticsearch(
            hosts=[{'host': 'elasticsearch_container', 'port': 9200, 'scheme': 'http'}])
        return es
    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}")
        es = None

        raise Exception("Elasticsearch connection not available")
