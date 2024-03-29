from django.forms import ModelForm, ValidationError, Form, ModelChoiceField, RadioSelect, CharField, TextInput
from musterdaten.models import Score, Modelsubject, Modeldataset


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


class EvaluateWizardFirstStepForm(Form):
    modelsubject = ModelChoiceField(widget=RadioSelect(attrs={'class': 'modelsubject'}), queryset=Modelsubject.objects.all(), required=False)


class EvaluateWizardSecondStepForm(Form):
    modeldataset = ModelChoiceField(widget=RadioSelect(attrs={'class': 'modeldataset'}), queryset=Modeldataset.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        kwargs.pop('top3', None)
        super().__init__(*args, **kwargs)


class EvaluateWizardThirdStepForm(Form):
    modeldataset = ModelChoiceField(widget=RadioSelect(attrs={'class': 'modeldataset'}), queryset=Modeldataset.objects.all(), required=False)


class EvaluateWizardFourthStepForm(Form):
    topic = CharField(widget=TextInput(attrs={"x-model":"topic"}),required=False)
    term = CharField(widget=TextInput(attrs={"x-bind:value":"term"}),required=False)
