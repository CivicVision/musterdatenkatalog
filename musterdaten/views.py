from django.views.generic import CreateView, TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

