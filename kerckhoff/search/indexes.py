from elasticsearch_dsl import DocType, Text, Keyword, Date

class PackageIndex(DocType):
    class Meta:
        index = 'package-index'
    slug = Keyword()
    package_set = Keyword()
    description = Text()
    cached_article_preview = Text()
    article_text = Text()
    publish_date = Date()