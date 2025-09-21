from typing import Optional

from src.voting.models import Voting


class GetCurrentVotingUseCase:
    def execute(self) -> Optional[Voting]:
        current_voting = Voting.objects.filter(
            active=True,
        ).first()

        return current_voting
