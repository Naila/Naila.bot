from django.views.generic import TemplateView


class CDNView(TemplateView):
    template_name = "cdn.html"
