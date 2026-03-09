



from alias.documents import SearchableAliasDocument


class AliasSearchService:

    def search(self, query):

        search = SearchableAliasDocument.search()

        search = search.query(
            "multi_match",
            query=query,
            fields=[
                "alias_en",
                "alias_iast"
            ],
            fuzziness="AUTO"
        )

        response = search.execute()

        results = []

        for hit in response:

            results.append({
                "id": hit.id,
                "alias_en": hit.alias_en,
                "alias_iast": hit.alias_iast
            })

        return results