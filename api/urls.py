from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ModeldatasetViewset

router = DefaultRouter()
router.register(r'modeldataset', ModeldatasetViewset)

app_name = 'api'
urlpatterns = [
    path('', include((router.urls)))
]
