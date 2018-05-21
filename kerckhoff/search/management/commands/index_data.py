from django.core.management.base import BaseCommand
from search.search import bulk_index_packages
import logging
from django.conf import settings

logger = logging.getLogger(settings.APP_NAME)

class Command(BaseCommand):
    help = 'Indexes data from our database into Elasticsearch'

    index_calls = {
        "package" : (bulk_index_packages, "Packages"),
    }

    def add_arguments(self, parser):
        parser.add_argument('type', nargs='*', type=str)

    def handle(self, *args, **options):
        logger.info("Bulk indexing data...")
        for index_fun, desc in self.index_calls.values():
            logger.info("Indexing %s... " % desc)
            index_fun()