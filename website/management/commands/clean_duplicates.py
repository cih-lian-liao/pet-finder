"""
Management command to remove duplicate pets from the database.
"""

from django.core.management.base import BaseCommand
from website.services import remove_duplicate_pets


class Command(BaseCommand):
    help = 'Remove duplicate pets from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be removed without actually removing anything',
        )

    def handle(self, *args, **options):
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('Dry run mode - no pets will be removed')
            )
            # TODO: Implement dry run logic
            self.stdout.write(
                self.style.SUCCESS('Dry run completed')
            )
        else:
            removed_count = remove_duplicate_pets()
            if removed_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully removed {removed_count} duplicate pets')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('No duplicate pets found')
                )
