from django.db.models import TextChoices


class ReportVoteType(TextChoices):
    UP = "UP"
    DOWN = "DOWN"
