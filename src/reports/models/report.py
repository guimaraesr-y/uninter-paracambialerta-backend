from django.db import models
from django.db.models import F
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from src.common.models import TimestampedModelMixin
from src.reports.choices.status import ReportStatus
from src.reports.models.category import Category


class Report(TimestampedModelMixin):
    """
    Represents a citizen's report about an urban issue.
    """

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
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
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

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status.upper()})"

    def apply_vote_delta(self, up_delta: int = 0, down_delta: int = 0):
        """
        Updates the counters atomically in the database.
        Uses F() to avoid concurrent read/write.
        """
        # Update via queryset to use F() (avoid loading instance if not necessary)
        self.__class__.objects.filter(pk=self.pk).update(
            upvotes_count=F('upvotes_count') + up_delta,
            downvotes_count=F('downvotes_count') + down_delta,
        )

        # Also updates the instance in memory for whoever called it
        self.refresh_from_db(fields=['upvotes_count', 'downvotes_count', 'updated_at'])
