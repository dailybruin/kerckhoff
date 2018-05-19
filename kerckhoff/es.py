import logging
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections

logger = logging.getLogger(settings.APP_NAME)

def init_es() -> Elasticsearch:
    logger.info("Connecting to elasticsearch...")
    # this creates the global connection pool to elasticsearch
    return connections.create_connection(hosts=[settings.ES_HOST,])