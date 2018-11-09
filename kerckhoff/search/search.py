from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from packages.models import Package

from .indexes import PackageIndex

elasticsearch_client = Elasticsearch(hosts=[settings.ES_HOST])


def bulk_index_packages():
    """
    Index all packages into Elasticsearch
    """
    PackageIndex.init()
    bulk(
        client=elasticsearch_client,
        actions=(b.indexing() for b in Package.objects.all().iterator()),
    )
