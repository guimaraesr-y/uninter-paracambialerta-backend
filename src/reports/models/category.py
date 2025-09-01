from django.db import models
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
