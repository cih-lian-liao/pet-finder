"""
Services for PetFinder scraping functionality.

This module contains business logic for scraping pet data from PetFinder.com
and handling the data processing and storage.
"""

import requests
import time
import logging
from typing import Dict, List, Optional, Tuple
from django.utils import timezone
from django.db import transaction
from .models import Pet
from .geocoding import get_coordinates_cached

logger = logging.getLogger(__name__)


class PetFinderAPIError(Exception):
    """Custom exception for PetFinder API errors."""
    pass


class PetFinderScraper:
    """
    Service class for scraping pet data from PetFinder.com.
    
    This class handles all interactions with the PetFinder API,
    including request formatting, error handling, and data processing.
    """
    
    BASE_URL = "https://www.petfinder.com/search/"
    DEFAULT_HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the scraper with custom headers if provided.
        
        Args:
            headers: Optional custom headers for requests
        """
        self.headers = headers or self.DEFAULT_HEADERS
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def build_search_url(self, city: str, state: str, animal: str, 
                        page: int = 1, limit: int = 100, distance: int = 100) -> str:
        """
        Build the search URL for PetFinder API.
        
        Args:
            city: City name for search
            state: State code for search
            animal: Animal type (dog, cat, etc.)
            page: Page number (default: 1)
            limit: Number of results per page (default: 100)
            distance: Search radius in miles (default: 100)
            
        Returns:
            Formatted URL string
        """
        # Ensure distance is a valid integer
        if distance is None:
            distance = 100
        distance = int(distance)
        
        # Ensure distance is within valid range
        if distance < 1:
            distance = 1
        elif distance > 500:
            distance = 500
        
        params = {
            'page': page,
            'limit[]': limit,
            'status': 'adoptable',
            'distance[]': distance,
            'type[]': animal,
            'sort[]': 'nearest',
            'location_slug[]': f'us%2F{state}%2F{city}',
            'include_transportable': 'true'
        }
        
        # Build query string
        query_parts = []
        for key, value in params.items():
            if value is not None:
                query_parts.append(f"{key}={value}")
        
        url = f"{self.BASE_URL}?{'&'.join(query_parts)}"
        logger.info(f"Built search URL with distance={distance} miles for {city}, {state}")
        return url
    
    def fetch_page_data(self, url: str) -> Dict:
        """
        Fetch data from a single page.
        
        Args:
            url: URL to fetch data from
            
        Returns:
            JSON response data
            
        Raises:
            PetFinderAPIError: If request fails or returns invalid data
        """
        try:
            logger.info(f"Fetching data from: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Validate response structure
            if 'result' not in data:
                raise PetFinderAPIError("Invalid response structure: missing 'result' key")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise PetFinderAPIError(f"Failed to fetch data: {e}")
        except ValueError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise PetFinderAPIError(f"Invalid JSON response: {e}")
    
    def extract_pet_data(self, pet_data: Dict) -> Dict:
        """
        Extract and normalize pet data from API response.
        
        Args:
            pet_data: Raw pet data from API
            
        Returns:
            Normalized pet data dictionary
        """
        animal = pet_data.get('animal', {})
        location = pet_data.get('location', {})
        
        # Extract basic information
        extracted = {
            'name': animal.get('name', '').strip(),
            'primary_breed': animal.get('primary_breed', {}).get('name', '').strip() if animal.get('primary_breed') else '',
            'is_mixed_breed': animal.get('is_mixed_breed', False),
            'primary_color': animal.get('primary_color', '').strip(),
            'age': animal.get('age', '').strip(),
            'sex': animal.get('sex', '').strip().lower(),
            'size': animal.get('size', '').strip().lower(),
            'coat_length': animal.get('coat_length', '').strip().lower(),
            'adoption_fee_waived': animal.get('adoption_fee_waived', False),
            'scraped_at': timezone.now(),
        }
        
        # Extract location information
        if location:
            address = location.get('address', {})
            extracted['location_city'] = address.get('city', '').strip()
            extracted['location_state'] = address.get('state', '').strip()
            extracted['location_zip'] = address.get('postal_code', '').strip()
            
            # Extract coordinates for distance calculation
            geo = location.get('geo', {})
            if geo:
                extracted['latitude'] = geo.get('latitude')
                extracted['longitude'] = geo.get('longitude')
        
        # Extract secondary breed
        if animal.get('secondary_breed'):
            extracted['secondary_breed'] = animal['secondary_breed'].get('name', '').strip()
        
        # Extract profile URL
        social_sharing = animal.get('social_sharing', {})
        if social_sharing and 'email_url' in social_sharing:
            extracted['profile_url'] = social_sharing['email_url'].strip()
        else:
            extracted['profile_url'] = ''
        
        # Extract photo URL
        if 'primary_photo_cropped_url' in animal:
            extracted['photo_url'] = animal['primary_photo_cropped_url'].strip()
        else:
            extracted['photo_url'] = ''
        
        # Extract adoption fee
        adoption_fee = animal.get('public_adoption_fee')
        if adoption_fee is not None:
            try:
                extracted['public_adoption_fee'] = float(adoption_fee)
            except (ValueError, TypeError):
                extracted['public_adoption_fee'] = None
        else:
            extracted['public_adoption_fee'] = None
        
        return extracted
    
    def save_pets_to_database(self, pets_data: List[Dict], search_city: str = None, 
                             search_state: str = None, max_distance: int = None) -> int:
        """
        Save multiple pets to database in a transaction with optional distance filtering.
        
        Args:
            pets_data: List of normalized pet data dictionaries
            search_city: Search city for distance filtering
            search_state: Search state for distance filtering
            max_distance: Maximum distance in miles (optional)
            
        Returns:
            Number of pets saved
        """
        saved_count = 0
        updated_count = 0
        filtered_count = 0
        
        # Get search coordinates for distance filtering
        search_lat, search_lon = None, None
        if search_city and search_state and max_distance:
            search_lat, search_lon = get_coordinates_cached(search_city, search_state)
            if not search_lat or not search_lon:
                logger.warning(f"Could not get coordinates for {search_city}, {search_state}")
        
        with transaction.atomic():
            for pet_data in pets_data:
                try:
                    # Apply distance filtering if coordinates are available
                    if search_lat and search_lon and max_distance:
                        pet_lat = pet_data.get('latitude')
                        pet_lon = pet_data.get('longitude')
                        
                        if pet_lat and pet_lon:
                            # Calculate distance using temporary Pet object
                            temp_pet = Pet(
                                latitude=pet_lat,
                                longitude=pet_lon
                            )
                            distance = temp_pet.calculate_distance(search_lat, search_lon)
                            
                            if distance is None or distance > max_distance:
                                filtered_count += 1
                                logger.debug(f"Filtered out pet {pet_data.get('name', 'Unknown')} - distance: {distance} miles")
                                continue
                        else:
                            # If pet has no coordinates, skip distance filtering
                            logger.debug(f"Pet {pet_data.get('name', 'Unknown')} has no coordinates, skipping distance filter")
                    
                    # Only check for exact profile_url matches to avoid removing legitimate duplicates
                    profile_url = pet_data.get('profile_url', '').strip()
                    
                    existing_pet = None
                    if profile_url:
                        # Only check by profile URL - this is the most reliable way to identify duplicates
                        existing_pet = Pet.objects.filter(profile_url=profile_url).first()
                    
                    # Get name and breed for logging
                    name = pet_data.get('name', 'Unknown')
                    breed = pet_data.get('primary_breed', 'Unknown')
                    
                    if existing_pet:
                        # Update existing pet with new data
                        for key, value in pet_data.items():
                            if key != 'id':  # Don't update the ID
                                setattr(existing_pet, key, value)
                        existing_pet.save()
                        updated_count += 1
                        logger.debug(f"Updated existing pet: {name} ({breed})")
                    else:
                        # Create new pet
                        Pet.objects.create(**pet_data)
                        saved_count += 1
                        logger.debug(f"Created new pet: {name} ({breed})")
                        
                except Exception as e:
                    logger.error(f"Failed to save pet {pet_data.get('name', 'Unknown')}: {e}")
                    continue
        
        logger.info(f"Database update complete: {saved_count} new pets, {updated_count} updated pets, {filtered_count} filtered out by distance")
        return saved_count
    
    def scrape_pets(self, city: str, state: str, animal: str, 
                   max_pages: int = 1, distance: int = 100) -> Tuple[int, int]:
        """
        Scrape pets from PetFinder with pagination support.
        
        Args:
            city: City name for search
            state: State code for search
            animal: Animal type
            max_pages: Maximum number of pages to scrape (default: 1)
            distance: Search radius in miles
            
        Returns:
            Tuple of (total_pages_found, pets_saved)
            
        Raises:
            PetFinderAPIError: If scraping fails
        """
        try:
            # Get first page to determine total pages
            first_page_url = self.build_search_url(city, state, animal, page=1, distance=distance)
            first_page_data = self.fetch_page_data(first_page_url)
            
            # Extract pagination info
            pagination = first_page_data.get('result', {}).get('pagination', {})
            total_pages = pagination.get('total_pages', 1)
            
            logger.info(f"Found {total_pages} pages for {animal}s in {city}, {state}")
            
            # Determine how many pages to actually scrape
            pages_to_scrape = min(max_pages, total_pages)
            
            all_pets_data = []
            
            # Scrape the determined number of pages
            for page_num in range(1, pages_to_scrape + 1):
                try:
                    if page_num == 1:
                        # Use data already fetched
                        page_data = first_page_data
                    else:
                        # Fetch additional pages
                        page_url = self.build_search_url(city, state, animal, page=page_num, distance=distance)
                        page_data = self.fetch_page_data(page_url)
                        time.sleep(2)  # Be respectful to the API
                    
                    # Extract pets from this page
                    animals = page_data.get('result', {}).get('animals', [])
                    
                    for animal_data in animals:
                        pet_data = self.extract_pet_data(animal_data)
                        all_pets_data.append(pet_data)
                    
                    logger.info(f"Extracted {len(animals)} pets from page {page_num}")
                    
                except Exception as e:
                    logger.error(f"Failed to scrape page {page_num}: {e}")
                    continue
            
            # Save all pets to database with distance filtering
            pets_saved = self.save_pets_to_database(
                all_pets_data, 
                search_city=city, 
                search_state=state, 
                max_distance=distance
            )
            
            logger.info(f"Successfully saved {pets_saved} pets from {pages_to_scrape} pages")
            
            return total_pages, pets_saved
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            raise PetFinderAPIError(f"Scraping failed: {e}")


def clear_all_pets() -> int:
    """
    Clear all pets from the database.
    
    Returns:
        Number of pets deleted
    """
    count = Pet.objects.count()
    Pet.objects.all().delete()
    logger.info(f"Deleted {count} pets from database")
    return count


def get_pets_with_filters(breed: str = None, sex: str = None, 
                         size: str = None, age: str = None) -> List[Pet]:
    """
    Get pets from database with optional filters.
    
    Args:
        breed: Filter by breed (partial match)
        sex: Filter by sex
        size: Filter by size
        age: Filter by age
        
    Returns:
        QuerySet of filtered pets
    """
    queryset = Pet.objects.all()
    
    if breed:
        queryset = queryset.filter(primary_breed__icontains=breed)
    
    if sex:
        queryset = queryset.filter(sex=sex)
    
    if size:
        queryset = queryset.filter(size=size)
    
    if age:
        queryset = queryset.filter(age__icontains=age)
    
    return queryset


def remove_duplicate_pets() -> int:
    """
    Remove duplicate pets from the database.
    
    This function identifies and removes pets with duplicate profile URLs
    or identical name + breed combinations, keeping the most recent one.
    
    Returns:
        Number of duplicates removed
    """
    from django.db.models import Count, Max
    
    removed_count = 0
    
    # Find duplicates by profile_url
    profile_duplicates = Pet.objects.values('profile_url').annotate(
        count=Count('id')
    ).filter(count__gt=1, profile_url__isnull=False).exclude(profile_url='')
    
    for duplicate in profile_duplicates:
        pets = Pet.objects.filter(profile_url=duplicate['profile_url']).order_by('-created_at')
        # Keep the first (most recent) and delete the rest
        for pet in pets[1:]:
            pet.delete()
            removed_count += 1
            logger.info(f"Removed duplicate pet by profile URL: {pet.name}")
    
    # Find duplicates by name + breed combination
    name_breed_duplicates = Pet.objects.values('name', 'primary_breed').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    for duplicate in name_breed_duplicates:
        pets = Pet.objects.filter(
            name=duplicate['name'],
            primary_breed=duplicate['primary_breed']
        ).order_by('-created_at')
        # Keep the first (most recent) and delete the rest
        for pet in pets[1:]:
            pet.delete()
            removed_count += 1
            logger.info(f"Removed duplicate pet by name+breed: {pet.name} ({pet.primary_breed})")
    
    logger.info(f"Removed {removed_count} duplicate pets from database")
    return removed_count
