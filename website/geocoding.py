"""
Geocoding utilities for converting city/state names to coordinates.
"""

import requests
import logging

logger = logging.getLogger(__name__)


class GeocodingService:
    """
    Service for geocoding city and state names to coordinates.
    
    This service uses the Nominatim API (OpenStreetMap) to convert
    city and state names to latitude and longitude coordinates.
    """
    
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    @staticmethod
    def get_coordinates(city: str, state: str) -> tuple:
        """
        Get latitude and longitude coordinates for a city and state.
        
        Args:
            city: City name
            state: State code or name
            
        Returns:
            Tuple of (latitude, longitude) or (None, None) if not found
        """
        try:
            # Format query for Nominatim
            query = f"{city}, {state}, USA"
            
            params = {
                'q': query,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'us'
            }
            
            headers = {
                'User-Agent': 'PetFinderApp/1.0 (Educational Purpose)'
            }
            
            logger.info(f"Geocoding: {query}")
            response = requests.get(
                GeocodingService.BASE_URL, 
                params=params, 
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                logger.info(f"Found coordinates: {lat}, {lon}")
                return lat, lon
            else:
                logger.warning(f"No coordinates found for: {query}")
                return None, None
                
        except Exception as e:
            logger.error(f"Geocoding failed for {city}, {state}: {e}")
            return None, None


# Common city coordinates cache for better performance
CITY_COORDINATES_CACHE = {
    ('Seattle', 'WA'): (47.6062, -122.3321),
    ('Atlanta', 'GA'): (33.7490, -84.3880),
    ('New York', 'NY'): (40.7128, -74.0060),
    ('Los Angeles', 'CA'): (34.0522, -118.2437),
    ('Chicago', 'IL'): (41.8781, -87.6298),
    ('Houston', 'TX'): (29.7604, -95.3698),
    ('Phoenix', 'AZ'): (33.4484, -112.0740),
    ('Philadelphia', 'PA'): (39.9526, -75.1652),
    ('San Antonio', 'TX'): (29.4241, -98.4936),
    ('San Diego', 'CA'): (32.7157, -117.1611),
    ('Dallas', 'TX'): (32.7767, -96.7970),
    ('San Jose', 'CA'): (37.3382, -121.8863),
    ('Austin', 'TX'): (30.2672, -97.7431),
    ('Jacksonville', 'FL'): (30.3322, -81.6557),
    ('Fort Worth', 'TX'): (32.7555, -97.3308),
    ('Columbus', 'OH'): (39.9612, -82.9988),
    ('Charlotte', 'NC'): (35.2271, -80.8431),
    ('San Francisco', 'CA'): (37.7749, -122.4194),
    ('Indianapolis', 'IN'): (39.7684, -86.1581),
    ('Washington', 'DC'): (38.9072, -77.0369),
}


def get_coordinates_cached(city: str, state: str) -> tuple:
    """
    Get coordinates with caching for common cities.
    
    Args:
        city: City name
        state: State code
        
    Returns:
        Tuple of (latitude, longitude) or (None, None) if not found
    """
    # Check cache first
    cache_key = (city.title(), state.upper())
    if cache_key in CITY_COORDINATES_CACHE:
        logger.info(f"Using cached coordinates for {city}, {state}")
        return CITY_COORDINATES_CACHE[cache_key]
    
    # Use geocoding service
    return GeocodingService.get_coordinates(city, state)
