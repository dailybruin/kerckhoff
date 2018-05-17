from elasticsearch_dsl.connections import connections
from django.conf import settings

# this creates the global connection pool to elasticsearch
connections.create_connection(hosts=[settings.ES_HOST])