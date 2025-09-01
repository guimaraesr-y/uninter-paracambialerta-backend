from django.db import models
from django.conf import settings


class Upvote(models.Model):
    report = models.ForeignKey(
        "reports.Report", on_delete=models.CASCADE
    )
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("report", "voter")


class Downvote(models.Model):
    report = models.ForeignKey("reports.Report", on_delete=models.CASCADE)
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("report", "voter")
