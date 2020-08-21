from django.forms import ModelForm, ValidationError

from musterdaten.models import Score


class ScoreForm(ModelForm):

    class Meta:
        model = Score
        fields = ['dataset', 'modeldataset']

    def clean(self):
        modeldataset = self.cleaned_data.get("modeldataset")
        dataset = self.cleaned_data.get("dataset")
        if not modeldataset:
            raise ValidationError("Invalid modeldataset.")
        if not dataset:
            raise ValidationError("Invalid dataset.")
