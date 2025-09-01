from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from src.reports.models.votes import Downvote, Upvote
from src.reports.models.category import Category


class Report(models.Model):
    """
    Represents a citizen's report about an urban issue.
    """

    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        RESOLVED = "RESOLVED", _("Resolved")
        ARCHIVED = "ARCHIVED", _("Archived")

    title = models.CharField(
        max_length=255,
        verbose_name=_("Title")
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    location = models.ForeignKey(
        "location.Location",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Location")
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Status")
    )
    upvotes_count = models.IntegerField(
        default=0,
        verbose_name=_("Upvotes count")
    )
    downvotes_count = models.IntegerField(
        default=0,
        verbose_name=_("Downvotes count")
    )
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="upvoted_reports",
        through="reports.Upvote",
        through_fields=("report", "voter"),
        verbose_name=_("Upvotes")
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="downvoted_reports",
        through="reports.Downvote",
        through_fields=("report", "voter"),
        verbose_name=_("Downvotes")
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name=_("Reporter")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reports",
        verbose_name=_("Category")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
