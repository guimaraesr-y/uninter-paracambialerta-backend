from django.core.management.base import BaseCommand
from src.reports.management.seed_categories import seed_categories


class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('[+] Seeding data...')
        run_seed(self)
        self.stdout.write('[+] Seeding done.')


def run_seed(self):
    seed_categories()
