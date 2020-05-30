from django.db import models
from django.utils.translation import gettext_lazy as _


class Reports(models.Model):
    reporter_id = models.BigIntegerField(
        verbose_name=_("Reporter ID"),
        help_text=_("ID of the user that made the report")
    )
    reason = models.TextField(
        verbose_name=_("Reason"),
        help_text=_("The reason for making the report")
    )
    proof = models.TextField(
        verbose_name=_("Proof"),
        help_text=_("The proof of the report")
    )
    nsfw = models.BooleanField(
        verbose_name=_("NSFW"),
        help_text=_("If the proof is NSFW")
    )
    user_id = models.BigIntegerField(
        verbose_name=_("User ID"),
        help_text=_("The user the report is against")
    )
    time_reported = models.DateTimeField(
        verbose_name=_("Time reported"),
        help_text=_("The time the report was made"),
        auto_now_add=True
    )
    approved = models.NullBooleanField(
        verbose_name=_("Approved"),
        help_text=_("If this report has been handled by an admin"),
        default=None
    )
    approver = models.TextField(
        verbose_name=_("Approver"),
        help_text=_("The staff member that approved the report")
    )


class Bans(models.Model):
    user_id = models.BigIntegerField(
        verbose_name=_("User ID"),
        help_text=_("The banned user")
    )
    reason = models.TextField(
        verbose_name=_("Reason"),
        help_text=_("The reason for the ban")
    )
    proof = models.TextField(
        verbose_name=_("Proof"),
        help_text=_("The proof of the ban")
    )
    nsfw = models.BooleanField(
        verbose_name=_("NSFW"),
        help_text=_("If the proof is NSFW")
    )
    created = models.DateTimeField(
        verbose_name=_("Created"),
        help_text=_("The time the ban was approved"),
        auto_now_add=True
    )
    report_id = models.BigIntegerField(
        verbose_name=_("Report ID"),
        help_text=_("The ID of the report associated with the ban")
    )
