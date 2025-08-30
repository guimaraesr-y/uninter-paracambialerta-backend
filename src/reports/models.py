from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Represents the category of a report, e.g., "Saneamento", "Infraestrutura".
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


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
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        verbose_name=_("Latitude")
    )
    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        verbose_name=_("Longitude")
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Status")
    )
    votes = models.IntegerField(
        default=0,
        verbose_name=_("Votes")
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