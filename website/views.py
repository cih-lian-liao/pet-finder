"""
Views for the Pet Finder application.

This module contains all the view functions and classes that handle
HTTP requests and responses for the pet finder website.
"""

import csv
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

from .models import Pet
from .forms import PetSearchForm, PetFilterForm
from .services import PetFinderScraper, PetFinderAPIError, clear_all_pets, get_pets_with_filters

logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    """
    Main homepage view that displays the search form and pet results.
    
    This view handles both GET and POST requests:
    - GET: Shows the search form and current pet results
    - POST: Processes search form and triggers pet scraping
    """
    template_name = 'homepage.html'
    
    def get_context_data(self, **kwargs):
        """Get context data for the template."""
        context = super().get_context_data(**kwargs)
        
        # Get filter form data from query parameters
        filter_form = PetFilterForm(self.request.GET)
        context['filter_form'] = filter_form
        
        # Get pets with optional filters
        pets = get_pets_with_filters(
            breed=filter_form.data.get('breed'),
            sex=filter_form.data.get('sex'),
            size=filter_form.data.get('size'),
            age=filter_form.data.get('age')
        )
        
        # Add pagination
        paginator = Paginator(pets, 20)  # 20 pets per page
        page_number = self.request.GET.get('page')
        context['pets'] = paginator.get_page(page_number)
        
        # Add search form
        context['search_form'] = PetSearchForm()
        
        # Add statistics
        context['total_pets'] = Pet.objects.count()
        context['recent_pets'] = Pet.objects.order_by('-created_at')[:5]
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests for pet searching."""
        form = PetSearchForm(request.POST)
        
        if form.is_valid():
            try:
                # Get form data
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                animal = form.cleaned_data['animal']
                distance = form.cleaned_data.get('distance')
                
                # Ensure distance is a valid integer
                if distance is None or distance == '':
                    distance = 100
                else:
                    distance = int(distance)
                
                # Initialize scraper
                scraper = PetFinderScraper()
                
                # Always clear existing data before new search to avoid duplicates
                deleted_count = clear_all_pets()
                if deleted_count > 0:
                    messages.info(request, f"Cleared {deleted_count} existing pets to ensure fresh results.")
                
                # Scrape pets (limit to 1 page for demo)
                total_pages, pets_saved = scraper.scrape_pets(
                    city=city,
                    state=state,
                    animal=animal,
                    max_pages=1,  # Limit to 1 page for demo
                    distance=distance
                )
                
                # Add success message
                messages.success(
                    request,
                    f"✅ Fresh search completed! Found {pets_saved} new pets in {city}, {state}. "
                    f"Total pages available: {total_pages}. Showing all available pets."
                )
                
                # Redirect to homepage to show results
                return redirect('home')
                
            except PetFinderAPIError as e:
                logger.error(f"Scraping error: {e}")
                messages.error(request, f"Failed to scrape pets: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                messages.error(request, "An unexpected error occurred. Please try again.")
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
        
        # Redirect back to homepage with error messages
        return redirect('home')


class ClearPetsView(View):
    """
    View to clear all pets from the database.
    
    This view handles the clearing of all pet data and provides
    user feedback through messages.
    """
    
    @method_decorator(require_http_methods(["POST"]))
    def post(self, request, *args, **kwargs):
        """Clear all pets from the database."""
        try:
            deleted_count = clear_all_pets()
            messages.success(request, f"Successfully cleared {deleted_count} pets from the database.")
        except Exception as e:
            logger.error(f"Error clearing pets: {e}")
            messages.error(request, "Failed to clear pets. Please try again.")
        
        return redirect('home')


class DownloadPetsView(View):
    """
    View to download pet data as a CSV file.
    
    This view generates a CSV file containing all pet data
    and serves it as a downloadable file.
    """
    
    def get(self, request, *args, **kwargs):
        """Generate and download CSV file of pet data."""
        try:
            # Get all pets
            pets = Pet.objects.all()
            
            # Create HTTP response with CSV content type
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="pets.csv"'}
            )
            
            # Create CSV writer
            writer = csv.writer(response)
            
            # Write header row
            writer.writerow([
                'ID', 'Name', 'Profile URL', 'Primary Breed', 'Secondary Breed',
                'Is Mixed Breed', 'Primary Color', 'Age', 'Sex', 'Size',
                'Coat Length', 'Photo URL', 'Adoption Fee', 'Fee Waived',
                'Created At', 'Updated At'
            ])
            
            # Write pet data
            for pet in pets:
                writer.writerow([
                    pet.id,
                    pet.name,
                    pet.profile_url or '',
                    pet.primary_breed or '',
                    pet.secondary_breed or '',
                    pet.is_mixed_breed,
                    pet.primary_color or '',
                    pet.age or '',
                    pet.sex or '',
                    pet.size or '',
                    pet.coat_length or '',
                    pet.photo_url or '',
                    pet.public_adoption_fee or '',
                    pet.adoption_fee_waived,
                    pet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    pet.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating CSV: {e}")
            messages.error(request, "Failed to generate CSV file. Please try again.")
            return redirect('home')


class PetDetailView(View):
    """
    View to display detailed information about a specific pet.
    
    This view shows comprehensive information about a single pet
    including all available details and photos.
    """
    
    def get(self, request, pet_id, *args, **kwargs):
        """Display pet detail page."""
        try:
            pet = Pet.objects.get(id=pet_id)
            context = {'pet': pet}
            return render(request, 'pet_detail.html', context)
        except Pet.DoesNotExist:
            messages.error(request, "Pet not found.")
            return redirect('home')
        except Exception as e:
            logger.error(f"Error retrieving pet {pet_id}: {e}")
            messages.error(request, "An error occurred while retrieving pet details.")
            return redirect('home')


class PetStatsView(View):
    """
    View to display statistics about the pet database.
    
    This view provides various statistics and analytics
    about the pets in the database.
    """
    
    def get(self, request, *args, **kwargs):
        """Display pet statistics."""
        try:
            # Calculate statistics
            total_pets = Pet.objects.count()
            breeds = Pet.objects.values_list('primary_breed', flat=True).distinct().count()
            mixed_breeds = Pet.objects.filter(is_mixed_breed=True).count()
            
            # Top breeds
            top_breeds = Pet.objects.values('primary_breed').annotate(
                count=Count('id')
            ).order_by('-count')[:10]
            
            # Sex distribution
            sex_distribution = Pet.objects.values('sex').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Size distribution
            size_distribution = Pet.objects.values('size').annotate(
                count=Count('id')
            ).order_by('-count')
            
            context = {
                'total_pets': total_pets,
                'total_breeds': breeds,
                'mixed_breeds': mixed_breeds,
                'top_breeds': top_breeds,
                'sex_distribution': sex_distribution,
                'size_distribution': size_distribution,
            }
            
            return render(request, 'pet_stats.html', context)
            
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            messages.error(request, "Failed to load statistics.")
            return redirect('home')


# Legacy function views for backward compatibility
def scrape(request):
    """Legacy view function - redirects to new class-based view."""
    return redirect('home')


def clear(request):
    """Legacy view function - redirects to new class-based view."""
    return redirect('home')


def download(request):
    """Legacy view function - redirects to new class-based view."""
    return redirect('home')