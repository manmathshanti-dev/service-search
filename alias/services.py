from alias.documents import SearchableAliasDocument
from ota.models import OTAService


class AliasSearchService:

    def search(self, query=None, from_alias=None):

        if query:

            query = query.strip().lower()

            search = SearchableAliasDocument.search()

            search = search.query(
                "multi_match",
                query=query,
                fields=[
                    "alias_en^2",
                    "alias_iast"
                ],
                fuzziness="AUTO"
            )

            search = search[:20]

            response = search.execute()

            return [
                {
                    "id": hit.id,
                    "alias_en": hit.alias_en,
                    "alias_iast": hit.alias_iast
                }
                for hit in response
            ]

        if from_alias:

            from_alias = from_alias.strip().lower()

            destinations = (
                OTAService.objects
                .filter(from_alias_en__iexact=from_alias)
                .values_list("to_alias_en", flat=True)
                .distinct()
            )

            destinations = list(destinations)

            if not destinations:
                return []

            search = SearchableAliasDocument.search()

            search = search.filter(
                "terms",
                alias_en=destinations
            )

            search = search[:50]

            response = search.execute()

            return [
                {
                    "id": hit.id,
                    "alias_en": hit.alias_en,
                    "alias_iast": hit.alias_iast
                }
                for hit in response
            ]

        search = SearchableAliasDocument.search()[:50]

        response = search.execute()

        return [
            {
                "id": hit.id,
                "alias_en": hit.alias_en,
                "alias_iast": hit.alias_iast
            }
            for hit in response
        ]