from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from musterdaten.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]
