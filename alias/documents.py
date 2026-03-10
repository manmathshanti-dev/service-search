from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from prediction_proxy.models import SearchableAlias


@registry.register_document
class SearchableAliasDocument(Document):

    class Index:
        name = "alias_search_alias"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = SearchableAlias

        fields = [
            "id",
            "alias_en",
            "alias_iast",
        ]