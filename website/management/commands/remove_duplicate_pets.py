"""
Django management command to remove duplicate pets based on name + breed combination.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from website.models import Pet
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Remove duplicate pets based on name + breed combination'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No pets will be deleted'))
        
        # Find duplicates by name + breed
        from django.db.models import Count
        duplicates = Pet.objects.values('name', 'primary_breed').annotate(
            count=Count('id')
        ).filter(count__gt=1).order_by('-count')
        
        total_duplicates = 0
        total_deleted = 0
        
        for dup in duplicates:
            name = dup['name']
            breed = dup['primary_breed']
            count = dup['count']
            
            self.stdout.write(f'\nFound {count} copies of {name} ({breed}):')
            
            # Get all pets with this name and breed
            pets = Pet.objects.filter(name=name, primary_breed=breed).order_by('created_at')
            
            # Keep the first one (oldest), delete the rest
            keep_pet = pets.first()
            delete_pets = pets[1:]
            
            self.stdout.write(f'  Keeping: ID {keep_pet.id} - {keep_pet.profile_url}')
            
            for pet in delete_pets:
                self.stdout.write(f'  {"Would delete" if dry_run else "Deleting"}: ID {pet.id} - {pet.profile_url}')
                total_duplicates += 1
                
                if not dry_run:
                    pet.delete()
                    total_deleted += 1
        
        if total_duplicates == 0:
            self.stdout.write(self.style.SUCCESS('No duplicate pets found!'))
        else:
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(f'\nDRY RUN: Would delete {total_duplicates} duplicate pets')
                )
                self.stdout.write('Run without --dry-run to actually delete them')
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'\nSuccessfully deleted {total_deleted} duplicate pets')
                )
