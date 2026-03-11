from rest_framework.views import APIView
from rest_framework.response import Response

from alias.services import AliasSearchService


class AliasSearchView(APIView):

    def get(self, request):

        query = request.GET.get("q")
        from_alias = request.GET.get("from")

        service = AliasSearchService()

        results = service.search(
            query=query,
            from_alias=from_alias
        )

        return Response(results)