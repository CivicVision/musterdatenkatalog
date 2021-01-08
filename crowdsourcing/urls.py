from django.urls import path

from crowdsourcing.views import IndexView, UeberView, ImpressumView, EvaluateFormView, FORMS

app_name = 'crowdsourcing'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ueber/', UeberView.as_view(), name='ueber'),
    path('impressum/', ImpressumView.as_view(), name='impressum'),
    path('score/', EvaluateFormView.as_view(FORMS), name='evaluate'),
]
