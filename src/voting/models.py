from datetime import timedelta
from django.utils import timezone
from django.db import models

from src.reports.models.votes import ReportVote


class Voting(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_to_be_selected = models.IntegerField(default=3)

    votes: "models.Manager[ReportVote]"

    class Meta:
        verbose_name = 'Voting'
        verbose_name_plural = 'Votings'

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'

    def time_left(self) -> timedelta:
        remaining = self.end_time - timezone.now()
        return max(remaining, timedelta(0))

    def get_winners(self) -> models.QuerySet[ReportVote]:
        votes = self.votes.order_by('-votes')
        return votes[:self.total_to_be_selected]
