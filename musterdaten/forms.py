from django.forms import ModelForm

from musterdaten.models import Score


class ScoreForm(ModelForm):

    class Meta:
        model = Score
        fields = ['dataset', 'modeldataset']
