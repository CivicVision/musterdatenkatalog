from django.views.generic import CreateView, TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class UeberView(TemplateView):
    template_name = "ueber.html"

