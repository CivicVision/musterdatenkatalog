import uuid

from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, TemplateView

from musterdaten.forms import ScoreForm
from musterdaten.models import Dataset, Modeldataset

class IndexView(TemplateView):
    template_name = "index.html"

class UeberView(TemplateView):
    template_name = "ueber.html"

class EvaluateFormView(FormView):
    form_class = ScoreForm
    success_url = reverse_lazy('evaluate')
    template_name = 'evaluate_formview.html'

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
