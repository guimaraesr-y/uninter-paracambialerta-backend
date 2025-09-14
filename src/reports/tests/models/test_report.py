import pytest

from src.reports.choices.status import ReportStatus
from src.reports.models import Report

from src.users.tests.fixtures import user
from src.location.tests.fixtures import location_factory


@pytest.mark.django_db
class TestReportModel:

    @pytest.fixture
    def report(self, user, location_factory):
        return Report(
            title="Test Report",
            description="This is a test report",
            reporter=user,
            location=location_factory()
        )

    def test_created(self, report):
        report.save()
        assert report.created_at
        assert report.status == ReportStatus.PENDING
