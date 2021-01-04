from django.views.generic import TemplateView
import requests
import requests_cache

requests_cache.install_cache(expire_after=300, include_get_headers=True)


class Minecraft(TemplateView):
    template_name = "testing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = requests.get("https://api.capes.dev/load/")
