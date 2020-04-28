from django.apps import apps
from django.contrib.admin import AdminSite
# from .models import MyModel
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _


class MyAdminSite(AdminSite):
    index_title = "• Admin"

    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404("The requested admin page does not exist.")
        # Sort the models alphabetically within each app.
        app_dict["models"].sort(key=lambda x: x["name"])
        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            "title": _("%(app)s administration") % {"app": app_name},
            "app_list": [app_dict],
            "app_label": app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            "admin/%s/app_index.html" % app_label,
            "admin/app_index.html"
        ], context)


admin_site = MyAdminSite(name="myadmin")
# admin_site.register(MyModel)
