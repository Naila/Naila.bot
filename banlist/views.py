from django.views.generic import ListView
from datetime import datetime
from .models import Bans
from collections import defaultdict


class BanlistHomeView(ListView):
    template_name = "banlist.html"
    model = Bans
    paginate_by = 1
    context_object_name = "bans"

    def get_queryset(self):
        return Bans.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bans = defaultdict(list)
        for ban in Bans.objects.all():
            bans[str(ban.user_id)].append({
                "reason": ban.reason,
                "proof": ban.proof,
                "nsfw": ban.nsfw,
                "created": ban.created,
            })
        context["bans"] = bans
        return context
