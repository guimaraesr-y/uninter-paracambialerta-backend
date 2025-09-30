from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models

from src.reports.models.votes import ReportVote


class Voting(models.Model):
    id: 'int'

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    active = models.BooleanField(default=False, blank=True, null=True)
    total_to_be_selected = models.IntegerField(default=3)

    votes: "models.Manager[ReportVote]"

    class Meta:
        verbose_name = 'Voting'
        verbose_name_plural = 'Votings'

    def __str__(self):
        return f'[{self.id}-{self.active}] {self.start_time} - {self.end_time}'

    def time_left(self) -> timedelta:
        remaining = self.end_time - timezone.now()
        return max(remaining, timedelta(0))

    def get_winners(self) -> models.QuerySet[ReportVote]:
        votes = self.votes.order_by('-votes')
        return votes[:self.total_to_be_selected]

    def stop(self):
        self.active = False
        self.save(update_fields=['active'])

    @staticmethod
    def stop_active_votings():
        Voting.objects.filter(active=True).update(active=False)

    @staticmethod
    def start_new_voting(start_time: datetime, end_time: datetime) -> 'Voting':
        return Voting.objects.create(
            start_time=start_time,
            end_time=end_time,
            active=True
        )
