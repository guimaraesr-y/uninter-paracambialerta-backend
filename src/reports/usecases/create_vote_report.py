from django.db import transaction
from django.db.models import Model
from dataclasses import dataclass
from typing import Optional, Tuple
from src.reports.choices.vote_type import ReportVoteType
from src.reports.models.report import Report
from src.reports.models.votes import ReportVote
from src.users.models import BasicUser


@dataclass
class CreateVoteResult:
    created: bool
    changed: bool
    up_delta: int
    down_delta: int
    report: Optional[Report] = None
    vote: Optional[ReportVote] = None


class CreateVoteReportUseCase:
    """
    UseCase responsible for creating/updating votes and applyin
    deltas to the Report's counters.
    """
    def __init__(
        self,
        report_id: int,
        user: BasicUser,
        vote_type: ReportVoteType
    ):
        self._report_id = report_id
        self._user = user
        self._vote_type = vote_type

    def execute(self) -> CreateVoteResult:
        """
        Outline the voting operation:
        1) Lock the report (select_for_update)
        2) Search for an existing vote
        3) Create or update a vote, calculate deltas
        4) Apply the deltas to the report (via atomic helper)
        """
        with transaction.atomic():
            report = self._lock_report(self._report_id)
            existing_vote = self._get_existing_vote(report, self._user)

            if existing_vote is None:
                vote = self._create_vote(report, self._user, self._vote_type)
                up_delta, down_delta = self._deltas_for_new(self._vote_type)
                created, changed = True, False
            else:
                # if the vote is repeated, nothing changes
                if self._is_same_vote(existing_vote, self._vote_type):
                    return CreateVoteResult(
                        created=False,
                        changed=False,
                        up_delta=0,
                        down_delta=0,
                        report=report,
                        vote=existing_vote
                    )

                old_vote_type = ReportVoteType(existing_vote.vote_type)
                vote = self._update_vote(existing_vote, self._vote_type)

                up_delta, down_delta = self._deltas_for_change(
                    old_vote_type=old_vote_type,
                    new_vote_type=self._vote_type,
                )
                created, changed = False, True

            # applies the deltas atomically to the report (helper in model)
            report.apply_vote_delta(up_delta=up_delta, down_delta=down_delta)

            return CreateVoteResult(
                created=created,
                changed=changed,
                up_delta=up_delta,
                down_delta=down_delta,
                report=report,
                vote=vote
            )

    # -------------------------
    # Auxiliary methods
    # -------------------------
    def _lock_report(self, report_id: int) -> Report:
        return Report.objects.select_for_update().get(pk=report_id)

    def _get_existing_vote(self, report: Report, user: Model) -> Optional[ReportVote]:
        return ReportVote.objects.filter(report=report, voter=user).first()

    def _create_vote(self, report: Report, user: Model, vote_type: ReportVoteType) -> ReportVote:
        return ReportVote.objects.create(report=report, voter=user, vote_type=vote_type)

    def _update_vote(self, vote: ReportVote, new_vote_type: ReportVoteType) -> ReportVote:
        vote.vote_type = new_vote_type
        vote.save(update_fields=['vote_type', 'updated_at'])
        return vote

    def _is_same_vote(self, vote: ReportVote, vote_type: ReportVoteType) -> bool:
        return vote.vote_type == vote_type

    def _deltas_for_new(self, vote_type: ReportVoteType) -> Tuple[int, int]:
        """
        Returns (up_delta, down_delta) when a new vote is created.
        """
        if vote_type == ReportVoteType.UP:
            return (1, 0)
        return (0, 1)

    def _deltas_for_change(
        self,
        old_vote_type: ReportVoteType,
        new_vote_type: ReportVoteType
    ) -> Tuple[int, int]:
        """
        Returns (up_delta, down_delta) when a vote changes type.
        Ex.: UP -> DOWN  = (-1, +1)
              DOWN -> UP  = (+1, -1)
        """
        if old_vote_type == ReportVoteType.UP and new_vote_type == ReportVoteType.DOWN:
            return (-1, 1)
        if old_vote_type == ReportVoteType.DOWN and new_vote_type == ReportVoteType.UP:
            return (1, -1)

        # default case (should not occur)
        return (0, 0)
