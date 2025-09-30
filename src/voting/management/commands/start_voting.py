from django.core.management.base import BaseCommand
from django.utils import timezone
import logging
from datetime import timedelta

from src.voting.models import Voting

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Starts a new weekly voting period."

    def handle(self, *args, **options):
        self.stdout.write("[+] Starting new voting period...")

        now = timezone.now()

        start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=5, hours=14, minutes=59)

        Voting.stop_active_votings()
        self.stdout.write("[+] Deactivated old voting periods.")

        new_voting = Voting.start_new_voting(
            start_time=start_time,
            end_time=end_time,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"[+] Successfully created new voting period: {new_voting.id} "
                f"from {new_voting.start_time.strftime('%Y-%m-%d %H:%M')} "
                f"to {new_voting.end_time.strftime('%Y-%m-%d %H:%M')}"
            )
        )
