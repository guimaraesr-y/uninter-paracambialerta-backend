from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from src.reports.choices.status import ReportStatus
from src.reports.choices.vote_type import ReportVoteType
from src.reports.models.votes import ReportVote
from src.reports.models.category import Category


class Report(models.Model):
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

    def create_vote(self, user, vote_type: ReportVoteType):
        vote = ReportVote.objects.filter(
            report=self,
            voter=user,
        ).first()

        if not vote:
            vote = ReportVote.objects.create(
                report=self,
                voter=user,
                vote_type=vote_type,
            )
        else:
            if vote_type == ReportVoteType.UP and vote.is_downvote:
                vote.vote_type = ReportVoteType.UP
                self.downvotes_count -= 1
            elif vote_type == ReportVoteType.DOWN and vote.is_upvote:
                vote.vote_type = ReportVoteType.DOWN
                self.upvotes_count -= 1

            vote.vote_type = vote_type
            vote.save(update_fields=["vote_type"])

        if vote_type == ReportVoteType.UP:
            self.upvotes_count += 1
        else:
            self.downvotes_count += 1
        self.save()
