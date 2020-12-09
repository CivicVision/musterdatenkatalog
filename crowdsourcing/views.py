import uuid

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from formtools.wizard.views import SessionWizardView

from crowdsourcing.forms import EvaluateWizardFirstStepForm, EvaluateWizardSecondStepForm, \
    EvaluateWizardThirdStepForm
from musterdaten.models import Dataset, Modelsubject, Score


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
        modelsubjects = self.object.top_3.select_related("modelsubject").values_list("modelsubject__id", flat=True)
        context["modelsubjects"] = Modelsubject.objects.filter(id__in=modelsubjects).distinct()
        return context


class ModelsubjectDatasetView(SingleObjectMixin, ListView):
    template_name = "modeldatasets_for_modelsubject.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Modelsubject.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modelsubject"] = self.object
        return context

    def get_queryset(self):
        return self.object.modeldataset_set.all()


FORMS = [("modelsubject", EvaluateWizardFirstStepForm),
         ("top3", EvaluateWizardSecondStepForm),
         ("modeldatasets", EvaluateWizardThirdStepForm)
         ]

TEMPLATES = {
    "modelsubject": "score.html",
    "top3": "score_dataset.html",
    "modeldatasets": "score_all_datasets.html"
}


def show_top3(wizard):
    cleaned_data_step_one = wizard.get_cleaned_data_for_step("modelsubject") or {}
    modelsubject = cleaned_data_step_one.get("modelsubject")
    if not modelsubject:
        return True

    top3_modelsubjects = wizard.get_form_kwargs("top3").get("top3")
    if not top3_modelsubjects:
        return False

    top3_modelsubject_ids = [m["modeldataset__modelsubject__id"] for m in top3_modelsubjects]
    return modelsubject.pk in top3_modelsubject_ids


def show_modeldatasets_for_modelsubjects(wizard):
    data_step_two = wizard.get_cleaned_data_for_step("top3") or {}
    modeldataset = data_step_two.get("modeldataset")
    second_condition = False if modeldataset else True
    return second_condition


class EvaluateFormView(SessionWizardView):
    condition_dict = {
        "modelsubject": True,
        "top3": show_top3,
        "modeldatasets": show_modeldatasets_for_modelsubjects
    }

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        data_step_two = self.get_cleaned_data_for_step("top3") or {}
        modeldataset_step_two = data_step_two.get("modeldataset")

        data_step_three = self.get_cleaned_data_for_step("modeldatasets") or {}
        modeldataset_step_three = data_step_three.get("modeldataset")

        modeldataset = modeldataset_step_two or modeldataset_step_three
        dataset_id = self.get_dataset().pk
        Score.objects.create(
            dataset_id=dataset_id,
            modeldataset=modeldataset,
            session_id=uuid.uuid4().__str__()[:32]
        )

        return HttpResponseRedirect(reverse_lazy("crowdsourcing:evaluate"))

    def get_dataset_by_id(self, pk):
        return Dataset.objects.get(pk=pk)

    def get_dataset(self):
        if "dataset_id" in self.storage.extra_data:
            return self.get_dataset_by_id(self.storage.extra_data.get("dataset_id"))
        return Dataset.objects.order_by("?").first()

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == "modelsubject":
            dataset = self.get_dataset_by_id(context.get("dataset_id"))
            top3 = dataset.top3_modelsubjects.all()
            context.update({
                "dataset": dataset,
                "top3": top3,
                })
        if self.steps.current == "top3":
            dataset = self.get_dataset_by_id(context.get("dataset_id"))
            data_step_one = self.get_cleaned_data_for_step("modelsubject") or {}
            modelsubject = data_step_one.get("modelsubject")
            top3_dataset = dataset.top3_modeldatasets.filter(modeldataset__modelsubject__id=modelsubject.pk).all()
            context.update({
                "dataset": dataset,
                "top3_dataset": top3_dataset,
            })
        if self.steps.current == "modeldatasets":
            data_step_one = self.get_cleaned_data_for_step("modelsubject") or {}
            modelsubject = data_step_one.get("modelsubject")
            all_datasets = modelsubject.modeldataset_set.all()
            context.update({
                "all_datasets": all_datasets,
                "modelsubject": modelsubject,
            })
        return context

    def get_form_initial(self, step):
        initial = {}
        if step == "modelsubject":
            dataset = self.get_dataset()
            self.storage.extra_data = {"dataset_id": dataset.pk}
            initial["dataset_id"] = dataset.pk
            initial["dataset"] = dataset
            initial["modelsubject"] = dataset.modeldataset.modelsubject
            initial["modeldataset"] = dataset.modeldataset
        return self.initial_dict.get(step, initial)

    def get_form_kwargs(self, step):
        dataset = self.get_dataset()
        if step == "top3":
            return {"top3": dataset.top3_modelsubjects.all()}
        return {}
