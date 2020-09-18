from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ModeldatasetViewset,
    ModelsubjectViewset,
    ScoreViewset,
    DatasetViewSet
)

router = DefaultRouter()
router.register(r'modeldataset', ModeldatasetViewset)
router.register(r'modelsubject', ModelsubjectViewset),
router.register(r'score', ScoreViewset),
router.register(r'dataset', DatasetViewSet),

app_name = 'api'
urlpatterns = [
    path('', include((router.urls)))
]
