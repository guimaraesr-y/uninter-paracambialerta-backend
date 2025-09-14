import pytest

from src.reports.models import Report, ReportVote
from src.reports.choices.vote_type import ReportVoteType
from src.reports.usecases import CreateVoteReportUseCase

from src.users.tests.fixtures import user  # noqa: F401
from src.location.tests.fixtures import location_factory  # noqa: F401


@pytest.mark.django_db
class TestCreateVoteUseCase:
    @pytest.fixture
    def report(self, user, location_factory):
        r = Report(
            title="Test Report",
            description="This is a test report",
            reporter=user,
            location=location_factory()
        )
        r.save()
        return r

    def test_create_upvote(self, report, user):
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=user,
            vote_type=ReportVoteType.UP,
        )
        result = usecase.execute()

        # resultado do usecase
        assert result.created is True
        assert result.changed is False
        assert result.up_delta == 1 and result.down_delta == 0

        # estado no banco
        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 0
        assert ReportVote.objects.filter(report=report, voter=user, vote_type=ReportVoteType.UP).exists()

    def test_create_downvote(self, report, user):
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=user,
            vote_type=ReportVoteType.DOWN,
        )
        result = usecase.execute()

        assert result.created is True
        assert result.changed is False
        assert result.up_delta == 0 and result.down_delta == 1

        report.refresh_from_db()
        assert report.upvotes_count == 0
        assert report.downvotes_count == 1
        assert ReportVote.objects.filter(report=report, voter=user, vote_type=ReportVoteType.DOWN).exists()

    def test_idempotent_same_vote(self, report, user):
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=user,
            vote_type=ReportVoteType.UP,
        )

        # primeiro voto
        first = usecase.execute()
        assert first.created is True

        # segundo voto igual (idempotente)
        second = usecase.execute()
        assert second.created is False
        assert second.changed is False

        assert second.up_delta == 0 and second.down_delta == 0

        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 0

    def test_change_down_to_up(self, report, user):
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=user,
            vote_type=ReportVoteType.DOWN,
        )

        # cria down
        res1 = usecase.execute()
        assert res1.created is True

        report.refresh_from_db()
        assert report.upvotes_count == 0
        assert report.downvotes_count == 1

        # muda para up
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=user,
            vote_type=ReportVoteType.UP,
        )
        res2 = usecase.execute()
        assert res2.created is False
        assert res2.changed is True

        assert res2.up_delta == 1 and res2.down_delta == -1

        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 0

        vote = ReportVote.objects.get(report=report, voter=user)
        assert vote.vote_type == ReportVoteType.UP

    def test_change_up_to_down(self, report, user):
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=user,
            vote_type=ReportVoteType.UP,
        )
        # cria up
        res1 = usecase.execute()
        assert res1.created is True

        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 0

        # muda para down
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=user,
            vote_type=ReportVoteType.DOWN,
        )
        res2 = usecase.execute()
        assert res2.created is False
        assert res2.changed is True
        assert res2.up_delta == -1 and res2.down_delta == 1

        report.refresh_from_db()
        assert report.upvotes_count == 0
        assert report.downvotes_count == 1

        vote = ReportVote.objects.get(report=report, voter=user)
        assert vote.vote_type == ReportVoteType.DOWN

    def test_multiple_users_votes(self, report, django_user_model):
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=report.reporter,
            vote_type=ReportVoteType.UP,
        )
        # reporter (primeiro user) upvote
        usecase.execute()

        # cria um segundo usuário
        user2 = django_user_model.objects.create_user(username="other", password="pass")
        usecase = CreateVoteReportUseCase(
            report_id=report.id,
            user=user2,
            vote_type=ReportVoteType.DOWN,
        )
        # outro usuário downvote
        usecase.execute()

        report.refresh_from_db()
        assert report.upvotes_count == 1
        assert report.downvotes_count == 1

        assert ReportVote.objects.filter(report=report).count() == 2
