from elasticsearch_dsl import Document, Text, Keyword, Date

class PackageIndex(Document):
    class Index:
        name = 'package-index'
    slug = Keyword()
    package_set = Keyword()
    description = Text()
    cached_article_preview = Text()
    article_text = Text()
    publish_date = Date()