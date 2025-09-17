from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import math


class Pet(models.Model):
    """
    Model representing a pet available for adoption.
    
    This model stores information about pets scraped from PetFinder.com,
    including their basic information, physical characteristics, and adoption details.
    """
    
    # Choices for standardized fields
    ANIMAL_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]
    
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]
    
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extra_large', 'Extra Large'),
    ]
    
    COAT_LENGTH_CHOICES = [
        ('short', 'Short'),
        ('medium', 'Medium'),
        ('long', 'Long'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        default="Unknown Pet",
        help_text="Pet's name"
    )
    profile_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to the pet's profile page"
    )
    photo_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to the pet's primary photo"
    )
    
    # Breed Information
    primary_breed = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Primary breed of the pet"
    )
    secondary_breed = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Secondary breed if mixed breed"
    )
    is_mixed_breed = models.BooleanField(
        default=False,
        help_text="Whether the pet is a mixed breed"
    )
    
    # Physical Characteristics
    primary_color = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Primary color of the pet"
    )
    age = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Age of the pet"
    )
    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        blank=True,
        null=True,
        help_text="Sex of the pet"
    )
    size = models.CharField(
        max_length=15,
        choices=SIZE_CHOICES,
        blank=True,
        null=True,
        help_text="Size of the pet"
    )
    coat_length = models.CharField(
        max_length=10,
        choices=COAT_LENGTH_CHOICES,
        blank=True,
        null=True,
        help_text="Length of the pet's coat"
    )
    
    # Adoption Information
    public_adoption_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Public adoption fee in USD"
    )
    adoption_fee_waived = models.BooleanField(
        default=False,
        help_text="Whether the adoption fee is waived"
    )
    
    # Location Information
    location_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City where the pet is located"
    )
    location_state = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="State where the pet is located"
    )
    location_zip = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="ZIP code where the pet is located"
    )
    latitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Latitude coordinate of pet location"
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Longitude coordinate of pet location"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="When this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this record was last updated"
    )
    scraped_at = models.DateTimeField(
        default=timezone.now,
        help_text="When this pet data was scraped"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['primary_breed']),
            models.Index(fields=['sex']),
            models.Index(fields=['size']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
    
    def __str__(self):
        return f"{self.name} ({self.primary_breed or 'Unknown Breed'})"
    
    @property
    def display_name(self):
        """Return a formatted display name for the pet."""
        if self.name:
            return self.name.title()
        return "Unknown Pet"
    
    @property
    def adoption_fee_display(self):
        """Return formatted adoption fee for display."""
        if self.adoption_fee_waived:
            return "Fee Waived"
        elif self.public_adoption_fee:
            return f"${self.public_adoption_fee}"
        return "Contact for Price"
    
    def calculate_distance(self, target_lat: float, target_lon: float) -> float:
        """
        Calculate distance between pet location and target location.
        
        Args:
            target_lat: Target latitude
            target_lon: Target longitude
            
        Returns:
            Distance in miles, or None if coordinates are not available
        """
        if not all([self.latitude, self.longitude, target_lat, target_lon]):
            return None
        
        # Haversine formula for calculating distance between two points
        R = 3959  # Earth's radius in miles
        
        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(target_lat)
        delta_lat = math.radians(target_lat - self.latitude)
        delta_lon = math.radians(target_lon - self.longitude)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    @property
    def location_display(self):
        """Return formatted location for display."""
        if self.location_city and self.location_state:
            return f"{self.location_city}, {self.location_state}"
        elif self.location_city:
            return self.location_city
        return "Location Unknown"
    
    def clean(self):
        """Validate model data."""
        from django.core.exceptions import ValidationError
        
        if self.is_mixed_breed and not self.secondary_breed:
            raise ValidationError({
                'secondary_breed': 'Secondary breed must be specified for mixed breed pets.'
            })
