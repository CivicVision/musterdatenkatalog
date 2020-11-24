from django.forms import ModelForm, ValidationError, Form, ModelChoiceField, BooleanField, TextInput, ChoiceField, \
        IntegerField, CharField, CheckboxInput

from musterdaten.models import Score, Modelsubject, Modeldataset, Dataset, Top3


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
    modelsubject = ModelChoiceField(queryset=Modelsubject.objects.all(), disabled=True)
    modeldataset = ModelChoiceField(queryset=Modeldataset.objects.all(), disabled=True)

    dataset_id = IntegerField(disabled=True)
    modelsubject_correct = BooleanField(widget=CheckboxInput(attrs={'x-bind:checked': 'modelsubject'}), required=False)
    modeldataset_correct = BooleanField(widget=CheckboxInput(attrs={'x-bind:checked': 'modeldataset'}), required=False)


class Top3Form(Form):
    top_3 = ModelChoiceField(queryset=Top3.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('top_3_queryset', None)
        super(Top3Form, self).__init__(*args, **kwargs)
        if queryset:
            self.fields['top_3'].queryset = queryset


class ModelsubjectsForm(Form):
    all_modelsubjects = ModelChoiceField(queryset=Modelsubject.objects.all())


class ModeldatasetsForm(Form):
    all_modeldatasets = ModelChoiceField(queryset=Modeldataset.objects.all())

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('all_modeldatasets', None)
        super(ModelsubjectsForm, self).__init__(*args, **kwargs)
        if queryset:
            self.fields['all_modeldatasets'].queryset = queryset
