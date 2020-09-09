from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ModeldatasetViewset, ModelsubjectViewset

router = DefaultRouter()
router.register(r'modeldataset', ModeldatasetViewset)
router.register(r'modelsubject', ModelsubjectViewset),

app_name = 'api'
urlpatterns = [
    path('', include((router.urls)))
]
