from django.urls import path

from crowdsourcing.views import IndexView, UeberView, EvaluateFormView

app_name = 'crowdsourcing'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ueber/', UeberView.as_view(), name='ueber'),
    path('evaluate/', EvaluateFormView.as_view(), name='evaluate'),
]
