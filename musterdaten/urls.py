from django.urls import include, path

from musterdaten import views

app_name = 'musterdaten'
urlpatterns = [
    path('ueber/', views.UeberView.as_view(), name='ueber'),
    path('', views.IndexView.as_view(), name='index'),
]
