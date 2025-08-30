from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class BasicUser(AbstractUser):
    """
    Custom user model that inherits from Django's AbstractUser.
    This model is the single source of truth for user information.
    """
    # You can add extra profile fields here in the future, for example:
    # bio = models.TextField(_("Bio"), blank=True)
    # phone_number = models.CharField(
    #     _("Phone Number"), max_length=20, blank=True
    # )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username
