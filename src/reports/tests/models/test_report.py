import pytest

from src.reports.choices.status import ReportStatus
from src.reports.models import Report

from src.users.tests.fixtures import user


@pytest.mark.django_db
class TestReportModel:

    @pytest.fixture
    def report(self, user):
        return Report(
            title="Test Report",
            description="This is a test report",
            latitude=37.7749,
            longitude=-122.4194,
            reporter=user,
        )

    def test_created(self, report):
        report.save()
        assert report.created_at
        assert report.status == ReportStatus.PENDING
