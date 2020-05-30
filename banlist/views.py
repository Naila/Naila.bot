from django.views.generic import TemplateView
from .models import Bans
from collections import defaultdict


class BanlistHomeView(TemplateView):
    template_name = "banlist.html"

    # model = Bans
    # paginate_by = 1
    # context_object_name = "bans"
    #
    # def get_queryset(self):
    #     return Bans.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bans = {}
        for ban in Bans.objects.all():
            if not str(ban.user_id) in bans:
                bans[str(ban.user_id)] = []
            bans[str(ban.user_id)].append({
                "reason": ban.reason,
                "proof": ban.proof,
                "nsfw": ban.nsfw,
                "created": ban.created,
            })
        context["bans"] = bans
        return context
