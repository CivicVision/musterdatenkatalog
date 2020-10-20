import uuid

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, TemplateView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from crowdsourcing.forms import ScoreForm
from musterdaten.models import Dataset, Modeldataset, Modelsubject

class IndexView(TemplateView):
    template_name = "index.html"


class UeberView(TemplateView):
    template_name = "ueber.html"


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


class EvaluateFormView(FormView):
    form_class = ScoreForm
    success_url = reverse_lazy('crowdsourcing:evaluate')
    template_name = 'score.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dataset = Dataset.objects.order_by('?').first()
        context["dataset"] = dataset
        context["modeldataset"] = dataset.modeldataset
        context["top_3"] = dataset.top_3
        context["all_modeldatasets"] = Modeldataset.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.session_id = uuid.uuid4().__str__()[:32]
        self.object.dataset = form.cleaned_data.get('dataset')
        self.object.modeldataset = form.cleaned_data.get('modeldataset')
        self.object.save()

        messages.success(self.request, 'Score added successfully!')

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response
