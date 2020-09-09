from django.db.models import Prefetch

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializer import ModeldatasetSerializer, ModelsubjectSerializer
from musterdaten.models import Modeldataset, Modelsubject, Dataset

class APIViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass

class ModeldatasetViewset(APIViewSet):
    queryset = (
            Modeldataset.objects.
            select_related("modelsubject", "leika").
            prefetch_related(
                Prefetch(
                    'datasets',
                    queryset=Dataset.objects.select_related('city', 'license')
                )
            )
    )
    serializer_class = ModeldatasetSerializer

    @action(detail=False, methods=['GET'])
    def search(self, request):
        q = request.query_params.get("q")
        datasets = Modeldataset.objects.filter(title__contains=q)
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)
