from django.apps import AppConfig
from django.conf import settings
from elasticsearch_dsl.connections import connections


class SearchConfig(AppConfig):
    name = "search"

    def ready(self):
        # by default 10 connections
        connections.configure(default={"host": settings.ES_HOST})
