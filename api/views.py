from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializer import ModeldatasetSerializer
from musterdaten.models import Dataset, Modeldataset

class ModeldatasetAPIView(ReadOnlyModelViewSet):
    queryset = Modeldataset.objects.all()
    serializer_class = ModeldatasetSerializer

    @action(detail=False, methods=['GET'])
    def search(self, request):
        q = request.query_params.get("q")
        datasets = Modeldataset.objects.filter(title__contains=q)
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)

