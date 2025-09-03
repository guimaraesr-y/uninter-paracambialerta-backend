import pytest

from src.reports.choices.status import ReportStatus
from src.reports.choices.vote_type import ReportVoteType
from src.reports.models import Report

from src.reports.models.votes import ReportVote
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

    def test_create_upvote(self, report, user):
        report.save()
        report.create_vote(user, ReportVoteType.UP)

        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 0
        assert report.votes.filter(
            voter=user,
            vote_type=ReportVoteType.UP
        ).exists()

    def test_create_downvote(self, report, user):
        report.save()
        report.create_vote(user, ReportVoteType.DOWN)
        report.refresh_from_db()

        assert report.upvotes_count == 0
        assert report.downvotes_count == 1
        assert ReportVote.objects.filter(
            report=report,
            voter=user,
            vote_type=ReportVoteType.DOWN
        ).exists()

    def test_switch_from_down_to_up(self, report, user):
        report.save()

        # Primeiro DOWN
        report.create_vote(user, ReportVoteType.DOWN)
        report.refresh_from_db()
        assert report.downvotes_count == 1
        assert report.upvotes_count == 0

        # Depois UP
        report.create_vote(user, ReportVoteType.UP)
        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 0
        vote = ReportVote.objects.get(report=report, voter=user)
        assert vote.vote_type == ReportVoteType.UP

    def test_switch_from_up_to_down(self, report, user):
        report.save()

        # Primeiro UP
        report.create_vote(user, ReportVoteType.UP)
        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 0

        # Depois DOWN
        report.create_vote(user, ReportVoteType.DOWN)
        report.refresh_from_db()
        assert report.upvotes_count == 0
        assert report.downvotes_count == 1
        vote = ReportVote.objects.get(report=report, voter=user)
        assert vote.vote_type == ReportVoteType.DOWN

    def test_multiple_users_votes(self, report, django_user_model):
        report.save()
        user2 = django_user_model.objects.create_user(
            username="other",
            password="pass",
        )

        report.create_vote(report.reporter, ReportVoteType.UP)
        report.create_vote(user2, ReportVoteType.DOWN)

        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 1
        assert ReportVote.objects.count() == 2
