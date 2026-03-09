from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from prediction_proxy.models import SearchableAlias



alias_index = Index("searchable_alias")

alias_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@registry.register_document
class SearchableAliasDocument(Document):

    class Index:
        name = "searchable_alias"

    class Django:
        model = SearchableAlias
        fields = [
            "id",
            "alias_en",
            "alias_iast",
        ]