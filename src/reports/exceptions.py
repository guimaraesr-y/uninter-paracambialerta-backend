from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class ReportException(APIException):
    status_code = 400
    default_detail = _("Report exception")
    default_code = "report_exception"


class NoCurrentVotingException(APIException):
    status_code = 400
    default_detail = _("There is no voting currently active.")
    default_code = "no_current_voting"


class ReportCannotBeVoted(APIException):
    status_code = 400
    default_detail = _("This report cannot be voted.")
    default_code = "report_cannot_be_voted"
