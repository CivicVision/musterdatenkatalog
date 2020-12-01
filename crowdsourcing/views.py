import uuid

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, TemplateView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from formtools.wizard.views import SessionWizardView

from crowdsourcing.forms import ScoreForm, EvaluateWizardFirstStepForm ,Top3Form, ModelsubjectsForm, ModeldatasetsForm
from musterdaten.models import Dataset, Modeldataset, Modelsubject, Score, Top3

class IndexView(TemplateView):
    template_name = "index.html"


class UeberView(TemplateView):
    template_name = "ueber.html"


class AllSubjectsView(ListView):
    template_name = "all_subjects.html"

    queryset = Modelsubject.objects.select_related()


class Top3SubjectView(DetailView):
    template_name = "top3_subject.html"

    queryset = Dataset.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modelsubjects = self.object.top_3.select_related('modelsubject').values_list('modelsubject__id', flat=True)
        context['modelsubjects'] = Modelsubject.objects.filter(id__in=modelsubjects).distinct()
        return context

class ModelsubjectDatasetView(SingleObjectMixin, ListView):
    template_name = "modeldatasets_for_modelsubject.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Modelsubject.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modelsubject'] = self.object
        return context

    def get_queryset(self):
        return self.object.modeldataset_set.all()

FORMS = [("dataset", EvaluateWizardFirstStepForm),
         ("top3", Top3Form),
         ("modelsubjects", ModelsubjectsForm),
         ("modeldatasets", ModeldatasetsForm)]

TEMPLATES = {"dataset": "score.html",
             "top3": "top3_subject.html",
             "modelsubjects": "all_subjects.html",
             "modeldatasets": "modeldatasets_for_modelsubject.html"}

def show_top3(wizard):
    cleaned_data_step_one = wizard.storage.get_step_data('dataset') or {}
    return not cleaned_data_step_one.get('dataset-modelsubject_correct') == 'on'


def show_all_modelsubjects(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('top3') or {}
    if not cleaned_data:
        return False
    return not cleaned_data.get('top_3')


def show_modeldatasets_for_modelsubjects(wizard):
    cleaned_data_step_one = wizard.storage.get_step_data('dataset') or {}
    return not cleaned_data_step_one.get('dataset-modeldataset_correct') == 'on' and not cleaned_data_step_one.get('dataset-modelsubject_correct') == 'on'


class EvaluateFormView(SessionWizardView):
    condition_dict = {
        'dataset': True,
        'top3': show_top3,
        'modelsubjects': show_all_modelsubjects,
        'modeldatasets': show_modeldatasets_for_modelsubjects
    }

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        data_step_one = self.get_cleaned_data_for_step('dataset') or {}

        dataset_id = data_step_one.get('dataset_id')
        if data_step_one.get('modeldataset_correct'):
            modeldataset = data_step_one.get('modeldataset')
        else:
            data_step_four = self.get_cleaned_data_for_step('modeldatasets')
            modeldataset = data_step_four.get('all_modeldatasets')

        Score.objects.create(
            dataset_id=dataset_id,
            modeldataset=modeldataset,
            session_id=uuid.uuid4().__str__()[:32]
        )

        return HttpResponseRedirect(reverse_lazy("crowdsourcing:evaluate"))

    def get_dataset_by_id(self, pk):
        return Dataset.objects.get(pk=pk)

    def get_dataset(self):
        if 'dataset_id' in self.storage.extra_data:
            return self.get_dataset_by_id(self.storage.extra_data.get('dataset_id'))
        return Dataset.objects.order_by('?').first()

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'dataset':
            dataset = self.get_dataset_by_id(context.get('dataset_id'))
            modelsubjects = dataset.top_3.select_related('modelsubject')
            top3 = dataset.top3_modelsubjects.all()
            top3_raw = Top3.objects.filter(dataset_id=dataset.pk).all()
            context.update({
                'dataset': dataset,
                'modeldataset': dataset.modeldataset,
                'modeldataset_score': top3[0],
                'top3': top3,
                'top3_alternatives': top3[1:],
                'top3_raw': top3_raw
                })
        if self.steps.current == 'top3':
            dataset = self.get_dataset_by_id(context.get('dataset_id'))
            modelsubjects = dataset.top_3.select_related('modelsubject').values_list('modelsubject__id', flat=True)
            context.update({
                'modelsubjects': Modelsubject.objects.filter(id__in=modelsubjects).distinct()
            })
        if self.steps.current == 'modelsubjects':
            context.update({
                'modelsubjects': Modelsubject.objects.select_related().all()
            })
        return context

    def get_form(self, step=None, data=None, files=None):
        dataset = self.get_dataset()
        kwargs = self.get_form_kwargs(step)

        if step == 'top3':
            # update the top_3 queryset to only show entries related to the dataset

            form_class = self.form_list[step]
            kwargs.update({
                'data': data,
                'files': files,
                'prefix': self.get_form_prefix(step, form_class),
                'initial': self.get_form_initial(step),
                'top_3_queryset': dataset.top_3.all()
            })
            return form_class(**kwargs)

        elif step == 'modeldatasets':
            # update the modeldatasets queryset to only show entries related to the chosen modelsubject

            form_class = self.form_list[step]
            step_three_data = self.get_cleaned_data_for_step('modelsubjects')
            if step_three_data:
                modelsubject = step_three_data.get('all_modelsubjects')
            else:
                step_one_data = self.get_cleaned_data_for_step('dataset')
                ## need to get the modeldataset some other way or 
                modelsubject = step_one_data.get('modelsubject')

            kwargs.update({
                'data': data,
                'files': files,
                'prefix': self.get_form_prefix(step, form_class),
                'initial': self.get_form_initial(step),
                'all_modeldatasets': modelsubject.modeldataset_set.all()
            })
            return form_class(**kwargs)

        return super(EvaluateFormView, self).get_form(step, data, files)

    def get_form_initial(self, step):
        initial = {}
        if step == 'dataset':
            dataset = self.get_dataset()
            self.storage.extra_data = {'dataset_id': dataset.pk}
            initial['dataset_id'] = dataset.pk
            initial['dataset'] = dataset
            initial['modelsubject'] = dataset.modeldataset.modelsubject
            initial['modeldataset'] = dataset.modeldataset
        return self.initial_dict.get(step, initial)
