from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ModeldatasetAPIView

router = DefaultRouter()
router.register(r'modeldataset', ModeldatasetAPIView)

app_name = 'api'
urlpatterns = [
    path('', include((router.urls)))
]
