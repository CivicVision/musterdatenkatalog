from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ModeldatasetViewset,
    ModelsubjectViewset,
    ScoreViewset
)

router = DefaultRouter()
router.register(r'modeldataset', ModeldatasetViewset)
router.register(r'modelsubject', ModelsubjectViewset),
router.register(r'score', ScoreViewset),

app_name = 'api'
urlpatterns = [
    path('', include((router.urls)))
]
