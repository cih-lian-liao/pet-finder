"""
Management command to test distance-based search functionality.
"""

from django.core.management.base import BaseCommand
from website.services import PetFinderScraper


class Command(BaseCommand):
    help = 'Test distance-based search functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--city',
            type=str,
            default='Seattle',
            help='City to search in'
        )
        parser.add_argument(
            '--state',
            type=str,
            default='WA',
            help='State to search in'
        )
        parser.add_argument(
            '--animal',
            type=str,
            default='dog',
            help='Animal type to search for'
        )
        parser.add_argument(
            '--distance',
            type=int,
            default=100,
            help='Search radius in miles'
        )

    def handle(self, *args, **options):
        city = options['city']
        state = options['state']
        animal = options['animal']
        distance = options['distance']
        
        self.stdout.write(
            self.style.SUCCESS(f'Testing search: {animal}s in {city}, {state} within {distance} miles')
        )
        
        scraper = PetFinderScraper()
        
        try:
            # Test URL building
            url = scraper.build_search_url(city, state, animal, distance=distance)
            self.stdout.write(f'Generated URL: {url}')
            
            # Test fetching data
            data = scraper.fetch_page_data(url)
            
            # Analyze results
            animals = data.get('result', {}).get('animals', [])
            total_count = data.get('result', {}).get('pagination', {}).get('total_count', 0)
            
            self.stdout.write(
                self.style.SUCCESS(f'Found {total_count} total {animal}s')
            )
            self.stdout.write(f'Retrieved {len(animals)} pets from first page')
            
            # Check if distance parameter is working
            if len(animals) > 0:
                self.stdout.write('\nFirst few pets:')
                for i, animal_data in enumerate(animals[:3]):
                    pet = animal_data.get('animal', {})
                    name = pet.get('name', 'Unknown')
                    distance_away = pet.get('distance', 'Unknown')
                    self.stdout.write(f'  {i+1}. {name} - Distance: {distance_away} miles')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error testing search: {e}')
            )
