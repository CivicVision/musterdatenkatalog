from django.urls import include, path

from musterdaten.views import IndexView, UeberView, EvaluateFormView

app_name = 'musterdaten'
urlpatterns = [
    path('ueber/', UeberView.as_view(), name='ueber'),
    path('', IndexView.as_view(), name='index'),
    path('evaluate/', EvaluateFormView.as_view(), name='evaluate'),
]
