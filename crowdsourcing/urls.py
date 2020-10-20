from django.urls import path

from crowdsourcing.views import IndexView, UeberView, Top3SubjectView, ModelsubjectDatasetView, EvaluateFormView

app_name = 'crowdsourcing'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ueber/', UeberView.as_view(), name='ueber'),
    path('score/top3_subject/<int:pk>/', Top3SubjectView.as_view(), name='top3_subject'),
    path('score/thema/<int:pk>/', ModelsubjectDatasetView.as_view(), name='modelsubject_modeldatasets'),
    path('score/', EvaluateFormView.as_view(), name='evaluate'),
]
