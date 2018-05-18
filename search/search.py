from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from django.conf import settings

from .indexes import PackageIndex
from packages.models import Package

def bulk_index_packages():
    """
    Index all packages into Elasticsearch
    """
    PackageIndex.init()
    es = Elasticsearch(hosts=[settings.ES_HOST,])
    bulk(client=es, actions=(b.indexing() for b in Package.objects.all().iterator()))

