from django.urls import include, path

from musterdaten import views

app_name = 'musterdaten'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
