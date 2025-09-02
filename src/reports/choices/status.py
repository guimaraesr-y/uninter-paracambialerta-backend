from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ReportStatus(TextChoices):
    PENDING = "PENDING", _("Pending")
    IN_PROGRESS = "IN_PROGRESS", _("In Progress")
    RESOLVED = "RESOLVED", _("Resolved")
    ARCHIVED = "ARCHIVED", _("Archived")
