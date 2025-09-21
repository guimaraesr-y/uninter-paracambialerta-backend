from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from src.common.models import TimestampedModelMixin
from src.reports.choices.vote_type import ReportVoteType
from src.reports.exceptions import ReportCannotBeVoted


class ReportVote(TimestampedModelMixin):
    """Represents a vote on a report."""

    report = models.ForeignKey(
        "reports.Report", related_name="votes", on_delete=models.CASCADE
    )
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    vote_type = models.CharField(choices=ReportVoteType.choices, max_length=4)

    class Meta:
        unique_together = ("report", "voter")

    def __str__(self):
        return f"{self.voter} voted {self.vote_type} on {self.report}"

    def save(self, *args, **kwargs) -> None:
        self._handle_can_be_voted()
        return super().save(*args, **kwargs)

    @property
    def is_upvote(self):
        return self.vote_type == ReportVoteType.UP

    @property
    def is_downvote(self):
        return self.vote_type == ReportVoteType.DOWN

    def _handle_can_be_voted(self) -> None:
        if not self.report.can_be_voted:
            raise ReportCannotBeVoted()
